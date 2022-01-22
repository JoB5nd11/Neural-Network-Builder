extends Control

export var line_color : Color = Color(0.3, 0.3, 0.3)
export var grid_size : int = 50
export var line_width : int = 1
export var opacity : float = 1.0
export var is_visible : bool = true

onready var top_bar = get_parent().get_node("Top Bar")
onready var inventory = get_parent().get_node("Inventory")

func _ready():
	set_visible(is_visible)
	
func _draw():
	if not is_visible:
		return
		
	for x in range(grid_size + 1, self.get_rect().size.x, grid_size):
		draw_line(Vector2(x, 0), Vector2(x, self.get_rect().size.y), line_color, line_width)
		
	for y in range(grid_size, self.get_rect().size.y, grid_size):
		draw_line(Vector2(0, y), Vector2(self.get_rect().size.x, y), line_color, line_width)

func to_grid_coords(neuron_position : Vector2):
	neuron_position.x -= inventory.get_rect().size.x
	neuron_position.y -= top_bar.get_rect().size.y
	
	neuron_position.x = round(neuron_position.x / grid_size)
	neuron_position.y = round(neuron_position.y / grid_size)
	
	#return (cell x, cell y)
	return neuron_position

func refresh():
	self.visible = false
	self.visible = true

func set_grid_size(value : int):
	self.grid_size = value

func set_visible(value : bool):
	is_visible = value
	self.visible = value

func snap_to_grid(neuron : Node):
	if neuron == null:
		return null
	
	#Law of Demeter
	var calculated_position : Vector2 = self.get_rect().position + neuron.grid_position * grid_size
	return calculated_position
