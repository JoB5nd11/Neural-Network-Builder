extends Control

signal _GridSize_changed

onready var grid_switch = get_node("Grid Settings/OnOff Switch")
onready var grid_size_input = get_node("Grid Settings/Grid Size Input")
onready var grid = get_parent().get_node("Grid")
onready var neuron_layer = get_parent().get_parent().get_node("Neuron Layer")

func _ready():
	grid_switch.connect('_OnOff_toggled', self, '_OnOff_toggled')
	grid_size_input.connect('_GridSize_changed', self, '_GridSize_changed')
	
func _OnOff_toggled(button_pressed):
	grid.set_visible(button_pressed)

func _GridSize_changed(value):
	grid.set_grid_size(value)
	neuron_layer.reposition_neuron()
	grid.refresh()
	emit_signal("_GridSize_changed", value)
	
