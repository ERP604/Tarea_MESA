import mesa
import numpy as np
import pandas as pd

def compute_gini(model):
    agent_clean = [agent.cleaned_cells for agent in model.schedule.agents if isinstance(agent, CleanAgent)]
    x = sorted(agent_clean)
    N = model.num_agents
    
    # Evitar división por cero
    if sum(x) == 0:
        return 0  # Retorna 0 si nadie ha limpiado aún
    
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B

class CleanAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cleaned_cells = 0
        self.movements = 0  # Contador de movimientos del agente

    def step(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        dirt = [obj for obj in cellmates if isinstance(obj, DirtAgent)]
        
        if dirt:
            self.model.grid.remove_agent(dirt[0])
            self.cleaned_cells += 1
            self.model.total_cleaned_cells += 1  # Incremento en celdas limpias totales
        else:
            possible_steps = self.model.grid.get_neighborhood(
                self.pos, moore=True, include_center=False
            )
            new_position = self.random.choice(possible_steps)
            self.model.grid.move_agent(self, new_position)
            self.movements += 1  # Incremento en movimientos del agente
            self.model.total_movements += 1  # Incremento en movimientos totales

class DirtAgent(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)

class CleanModel(mesa.Model):
    def __init__(self, N, width, height, dirty_percentage, max_steps):
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.dirty_percentage = dirty_percentage
        self.max_steps = max_steps
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True

        self.total_cleaned_cells = 0  # Contador de celdas limpias
        self.total_movements = 0      # Contador de movimientos totales
        self.cleaned_percentage = 0   # Porcentaje de celdas limpias

        # Crear agentes de limpieza
        for i in range(self.num_agents):
            a = CleanAgent(i, self)
            self.schedule.add(a)
            self.grid.place_agent(a, (1, 1))

        # Crear suciedad en la cuadrícula
        total = width * height
        num_dirty_cells = int(total * (self.dirty_percentage / 100)) 
        dirty_positions = self.random.sample([(x, y) for x in range(width) for y in range(height)], num_dirty_cells)

        for i, pos in enumerate(dirty_positions, start=self.num_agents):
            dirt = DirtAgent(i, self)
            self.grid.place_agent(dirt, pos)

        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"CleanedCells": "cleaned_cells"}
        )

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()

        # Calcular el porcentaje de celdas limpias
        total_cells = self.grid.width * self.grid.height
        self.cleaned_percentage = (self.total_cleaned_cells / total_cells) * 100

        # Terminar la simulación si se ha limpiado todo o se alcanza el límite de pasos
        if self.total_cleaned_cells == int(total_cells * (self.dirty_percentage / 100)) or self.schedule.steps >= self.max_steps:
            self.running = False
            print(f"Tiempo total: {self.schedule.steps} pasos")
            print(f"Porcentaje de celdas limpias: {self.cleaned_percentage}%")
            print(f"Movimientos totales: {self.total_movements}")
