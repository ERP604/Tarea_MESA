import mesa
from mesa.visualization.modules import ChartModule, TextElement
from clean_robot import *

class ModelStats(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        total_steps = model.schedule.steps
        cleaned_percentage = (model.total_cleaned_cells / (model.grid.width * model.grid.height)) * 100
        total_movements = model.total_movements
        return f"Pasos totales: {total_steps} | Porcentaje de celdas limpias: {cleaned_percentage:.2f}% | Movimientos totales: {total_movements}"

def agent_portrayal(agent):
    if isinstance(agent, CleanAgent):
        portrayal = {
            "Shape": "circle",
            "Filled": "true",
            "Layer": 0,
            "Color": "blue",
            "r": 0.5
        }
    elif isinstance(agent, DirtAgent):
        portrayal = {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "Color": "brown",
            "w": 0.5,
            "h": 0.5
        }
    return portrayal

# Agregar una visualización de la cuadrícula y de las estadísticas
grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
stats_text = ModelStats()

# Configuración del servidor
server = mesa.visualization.ModularServer(
    CleanModel,
    [grid, stats_text],
    "Modelo de Limpieza",
    {"N": 10, "width": 10, "height": 10, "dirty_percentage": 100, "max_steps": 50}
)

server.port = 8522
server.launch()
