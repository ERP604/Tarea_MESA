# clean_robot_server.py
# Descripción breve: Servidor para la visualización del modelo de limpieza con agentes.
# Autor: José Eduardo Rosas Ponciano, Emiliano Caballero Mendoza
# Fecha de creación/modificación: 08/11/2024

import mesa
from mesa.visualization.modules import ChartModule, TextElement
from clean_robot import *

class ModelStats(TextElement):
    """Elemento de texto para mostrar estadísticas del modelo en la visualización."""
    
    def __init__(self):
        pass

    def render(self, model):
        totalSteps = model.schedule.steps
        cleanedPercentage = (model.totalCleanedCells / (model.grid.width * model.grid.height)) * 100
        totalMovements = model.totalMovements
        return f"Pasos totales: {totalSteps} | Porcentaje de celdas limpias: {cleanedPercentage:.2f}% | Movimientos totales: {totalMovements}"

def agentPortrayal(agent):
    """Define la apariencia de los agentes en la visualización."""
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

grid = mesa.visualization.CanvasGrid(agentPortrayal, 10, 10, 500, 500)
statsText = ModelStats()

server = mesa.visualization.ModularServer(
    CleanModel,
    [grid, statsText],
    "Modelo de Limpieza",
    {"numAgents": 10, "width": 10, "height": 10, "dirtyPercentage": 100, "maxSteps": 50}
)

server.port = 8522
server.launch()
