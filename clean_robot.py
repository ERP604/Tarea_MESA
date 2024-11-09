# clean_robot.py
# Descripción breve: Simulación de limpieza con agentes que remueven suciedad de una cuadrícula.
# Autor: Emiliano Caballero Mendoza, José Eduardo Rosas Ponciano
# Fecha de creación/modificación: 08/11/2024

import mesa
import numpy as np
import pandas as pd

def computeGini(model):
    """Calcula el coeficiente de Gini basado en las celdas limpiadas por cada agente."""
    agentClean = [agent.cleanedCells for agent in model.schedule.agents if isinstance(agent, CleanAgent)]
    x = sorted(agentClean)
    numAgents = model.numAgents
    
    if sum(x) == 0:
        return 0  # Retorna 0 si nadie ha limpiado aún
    
    B = sum(xi * (numAgents - i) for i, xi in enumerate(x)) / (numAgents * sum(x))
    return 1 + (1 / numAgents) - 2 * B

class CleanAgent(mesa.Agent):
    """Agente de limpieza que limpia celdas sucias en la cuadrícula."""
    
    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)
        self.cleanedCells = 0
        self.movements = 0

    def step(self):
        """Define el comportamiento del agente en cada paso: limpiar o moverse."""
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        dirt = [obj for obj in cellmates if isinstance(obj, DirtAgent)]
        
        if dirt:
            self.model.grid.remove_agent(dirt[0])
            self.cleanedCells += 1
            self.model.totalCleanedCells += 1
        else:
            possibleSteps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
            newPosition = self.random.choice(possibleSteps)
            self.model.grid.move_agent(self, newPosition)
            self.movements += 1
            self.model.totalMovements += 1

class DirtAgent(mesa.Agent):
    """Agente que representa suciedad en una celda específica."""
    
    def __init__(self, uniqueId, model):
        super().__init__(uniqueId, model)

class CleanModel(mesa.Model):
    """Modelo de simulación para agentes de limpieza y suciedad en una cuadrícula."""
    
    def __init__(self, numAgents, width, height, dirtyPercentage, maxSteps):
        self.numAgents = numAgents
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.dirtyPercentage = dirtyPercentage
        self.maxSteps = maxSteps
        self.schedule = mesa.time.RandomActivation(self)
        self.running = True

        self.totalCleanedCells = 0
        self.totalMovements = 0
        self.cleanedPercentage = 0

        for i in range(self.numAgents):
            agent = CleanAgent(i, self)
            self.schedule.add(agent)
            self.grid.place_agent(agent, (1, 1))

        totalCells = width * height
        numDirtyCells = int(totalCells * (self.dirtyPercentage / 100)) 
        dirtyPositions = self.random.sample([(x, y) for x in range(width) for y in range(height)], numDirtyCells)

        for i, pos in enumerate(dirtyPositions, start=self.numAgents):
            dirt = DirtAgent(i, self)
            self.grid.place_agent(dirt, pos)

        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": computeGini},
            agent_reporters={"CleanedCells": "cleanedCells"}
        )

    def step(self):
        """Ejecuta un paso en el modelo, recopilando datos y controlando el final de la simulación."""
        self.datacollector.collect(self)
        self.schedule.step()

        totalCells = self.grid.width * self.grid.height
        self.cleanedPercentage = (self.totalCleanedCells / totalCells) * 100

        if self.totalCleanedCells == int(totalCells * (self.dirtyPercentage / 100)) or self.schedule.steps >= self.maxSteps:
            self.running = False
            print(f"Tiempo total: {self.schedule.steps} pasos")
            print(f"Porcentaje de celdas limpias: {self.cleanedPercentage}%")
            print(f"Movimientos totales: {self.totalMovements}")
