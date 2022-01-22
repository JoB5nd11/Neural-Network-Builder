extends Node

onready var bg = get_node("Background")
onready var top_bar = get_node("Top Bar")
onready var inventory = get_node("Inventory")
onready var grid = get_node("Grid")
onready var neuron_layer = get_parent().get_node("Neuron Layer")

var window_x : int = 0
var window_y : int = 0
	
func _ready():
	get_tree().get_root().connect("size_changed", self, "resize_objects")
	set_grid_pos()
	
func resize_objects():
	window_x = get_viewport().size.x
	window_y = get_viewport().size.y
	
	bg.set_size(Vector2(window_x, window_y))
	top_bar.set_size(Vector2(window_x, top_bar.get_rect().size.y))
	inventory.set_size(Vector2(inventory.get_rect().size.x, window_y))
	grid.set_size(Vector2(window_x - grid.get_rect().position.x, window_y - grid.get_rect().position.y))
	#neuron_layer.set_size(Vector2(window_x - neuron_layer.get_rect().position.x, window_y - neuron_layer.get_rect().position.y))
	
	
func set_grid_pos():
	grid.set_position(Vector2(inventory.get_rect().position.x + inventory.get_rect().size.x, 
							  top_bar.get_rect().position.y + top_bar.get_rect().size.y))
	
