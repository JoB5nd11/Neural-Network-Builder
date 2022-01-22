extends Node2D

onready var image : Sprite = get_node("Image")
onready var ID_label : Label = get_node("Image/ID")

var texture_paths = {
	"Input": load("res://assets/Sprites/input_neuron.png"),
	"Hidden": load("res://assets/Sprites/hidden_neuron.png"),
	"Output": load("res://assets/Sprites/output_neuron.png")
}
var is_in_hand : bool = false
var grid_position : Vector2 = Vector2()

var ID : int

func _init():
	return self
	
func _ready():
	return self

func init(type : String, grid_size : int, id : int):
	self.ID = id
	ID_label.text = str(id)
	
	image.texture = texture_paths[type]
	image.scale = Vector2(grid_size - 1, grid_size - 1) / image.get_texture().get_size()
	image.position = image.position + Vector2(1, 1)
	
	return self

func resize_to_grid(grid_size : int):
	image.scale = Vector2(grid_size - 1, grid_size - 1) / image.get_texture().get_size()
