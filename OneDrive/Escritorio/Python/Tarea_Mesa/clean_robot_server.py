import mesa
from clean_robot import * 

def agent_portrayal(agent):
    if isinstance(agent, CleanAgent):
        portrayal = {
            "Shape": "circle",
            "Filled" : "true",
            "Layer" : 0,
            "Color":"blue",
            "r": 0.5
        }
    elif isinstance(agent,DirtAgent):
        portrayal = {
            "Shape": "rect",
            "Filled" : "true",
            "Layer" : 0,
            "Color":"brown",
            "w": 0.5,
            "h" : 0.5
        }

    return portrayal
    

grid = mesa.visualization.CanvasGrid(
    agent_portrayal, 10,10,500,500
)

server = mesa.visualization.ModularServer(
    CleanModel,
    [grid],
    "Clean Model",
    {"N":10, "width":10,"height":10,"dirty_percentage":40,
    "max_steps":50}
)

server.port = 8522
server.launch()