extends Node

export var show_id : bool = true

export var connection_color : Color = Color(1, 1, 1, 1)
export var connection_width : int = 2

onready var grid = get_parent().get_node("UI Elements/Grid")
onready var inventory = get_parent().get_node("UI Elements/Inventory")
onready var top_bar = get_parent().get_node("UI Elements/Top Bar")

var neurons = []
var neuron_connections = []
var current_neuron_id : int = 0

var is_neuron_in_hand : bool = false
var neuron_in_hand : Node2D

var is_dragging : bool = false
var current_dragging_neurons = [null, null]

func _ready():
	inventory.connect('_InputNeuron_created', self, '_InputNeuron_created')
	inventory.connect('_HiddenNeuron_created', self, '_HiddenNeuron_created')
	inventory.connect('_OutputNeuron_created', self, '_OutputNeuron_created')
	top_bar.connect('_GridSize_changed', self, '_GridSize_changed')

func _process(_delta):
	if is_neuron_in_hand:
		neuron_in_hand.z_index = 999
		neuron_in_hand.set_position(get_viewport().get_mouse_position() - (Vector2(grid.grid_size, grid.grid_size) / 2))
		redraw_lines_from_neuron(neuron_in_hand)

func _input(event):
	#Neuron in hand gets placed
	if event is InputEventMouseButton and event.pressed and event.button_index == BUTTON_MIDDLE and len(neurons) > 0:
		print(get_neuron_in_cell(get_click_grid_cell(event.position)))
		print_all_neuron_grid_pos()
	if event is InputEventMouseButton and not event.pressed and event.button_index == BUTTON_LEFT and is_neuron_in_hand and not is_dragging \
	and (get_neuron_in_cell(get_click_grid_cell(event.position)) == null or get_neuron_in_cell(get_click_grid_cell(event.position)) == neuron_in_hand):
		neuron_in_hand.grid_position = grid.to_grid_coords(neuron_in_hand.position)
		
		if grid.is_visible:
			neuron_in_hand.position = grid.snap_to_grid(neuron_in_hand)
			redraw_lines_from_neuron(neuron_in_hand)

		neuron_in_hand.z_index = 1 #has to be 1 because connection lines are at 0
		if not is_there_duplicate(neuron_in_hand):
			neurons.append(neuron_in_hand)
		neuron_in_hand = null
		is_neuron_in_hand = false
	
	#Draw Line or pick up neuron
	elif event is InputEventMouseButton and event.button_index == BUTTON_LEFT and not is_neuron_in_hand \
	and get_neuron_in_cell(get_click_grid_cell(event.position)) != null:
		#Drag start
		if event.pressed:
			is_dragging = true
			current_dragging_neurons[0] = get_neuron_in_cell(get_click_grid_cell(event.position))
		#Drag stop
		elif not event.pressed and is_dragging:
			is_dragging = false
			current_dragging_neurons[1] = get_neuron_in_cell(get_click_grid_cell(event.position))
			
			#Draggin started on neuron and ended on neuron and both are different
			if current_dragging_neurons[0] != null and current_dragging_neurons[1] != null \
			and current_dragging_neurons[0] != current_dragging_neurons[1]:
				connect_neurons(current_dragging_neurons)
				
			#Both neuron were the same -> pick up	
			elif current_dragging_neurons[0] == current_dragging_neurons[1]:
				current_dragging_neurons = [null, null]
				neuron_in_hand = get_neuron_in_cell(get_click_grid_cell(event.position))
				if neuron_in_hand != null:
					is_neuron_in_hand = true
		
	#Escape to delete neuron
	elif event is InputEventKey and event.scancode == KEY_ESCAPE and not event.pressed and is_neuron_in_hand:
		delete_neuron(neuron_in_hand)


func _InputNeuron_created():
	neuron_in_hand = load_neuron("Input", grid.grid_size)
	self.add_child(neuron_in_hand)


func _HiddenNeuron_created():
	neuron_in_hand = load_neuron("Hidden", grid.grid_size)
	self.add_child(neuron_in_hand)


func _OutputNeuron_created():
	neuron_in_hand = load_neuron("Output", grid.grid_size)
	self.add_child(neuron_in_hand)


func _GridSize_changed(value):
	for neuron in self.neurons:
		redraw_lines_from_neuron(neuron)
		

func are_neurons_connected(neurons):
	for connection in neuron_connections:
		if (connection[0] == neurons[0] and connection[1] == neurons[1]) \
		or (connection[0] == neurons[1] and connection[1] == neurons[0]):
			return true
	return false


func connect_neurons(neurons):
	neurons = draw_connection(neurons)
	if neurons != null:
		neuron_connections.append(neurons)
	current_dragging_neurons = [null, null]


func delete_connection(neurons):
	for connection in self.neuron_connections:
		if (connection[0] == neurons[0] and connection[1] == neurons[1]) \
		or (connection[0] == neurons[1] and connection[1] == neurons[0]):
			connection[2].visible = false


func delete_neuron(neuron : Node):
	self.remove_child(neuron)
	if get_neuron_index(neuron):
		neurons.remove(get_neuron_index(neuron))
	
	for connection in self.neuron_connections:
		if connection[0] == neuron or connection[1] == neuron:
			delete_connection([connection[0], connection[1]])
	
	#delete all connection with line marked as invisible
	#if connection element is erased in delete_neuron the loop above cannot run through all connections
	for connection in self.neuron_connections:
		if not connection[2].visible:
			self.neuron_connections.erase(connection)
			
	neuron = null
	is_neuron_in_hand = false


func draw_connection(neurons):
	if not are_neurons_connected(neurons):
		var line2d = Line2D.new()
		line2d.add_point(neurons[0].position + Vector2(grid.grid_size / 2, grid.grid_size / 2))
		line2d.add_point(neurons[1].position + Vector2(grid.grid_size / 2, grid.grid_size / 2))
		line2d.default_color = connection_color
		line2d.width = connection_width
		line2d.z_index = 0
		neurons.append(line2d)
		self.add_child(line2d)
		return neurons
	else:
		delete_connection(neurons)
		for connection in self.neuron_connections:
			if not connection[2].visible:
				self.neuron_connections.erase(connection)
		return null


func get_click_grid_cell(mouse_position : Vector2):
	return grid.to_grid_coords(mouse_position - Vector2(grid.grid_size / 2, grid.grid_size / 2))


func get_neuron_in_cell(cell_position : Vector2):
	for neuron in self.neurons:
		if neuron.grid_position == cell_position:
			return neuron
	return null
	
	
func get_neuron_index(neuron : Node):
	for i in range(len(self.neurons)):
		if neurons[i] == neuron:
			return i
	return null


func is_there_duplicate(neuron):
	for n in self.neurons:
		if n.ID == neuron.ID:
			return true
	return false


func load_neuron(type : String, grid_size : int):
	var neuron = load("res://scenes/Objects/Neuron.tscn").instance()._ready().init(type, grid_size, current_neuron_id)
	current_neuron_id += 1
	is_neuron_in_hand = true
	
	if show_id:
		neuron.ID_label.visible = true
	else:
		neuron.ID_label.visible = false
		
	return neuron


func print_all_neuron_grid_pos():
	print("Number of Neurons: ", len(self.neurons))
	for neuron in self.neurons:
		print("Neuron ", neuron.ID, ": ",  neuron.grid_position)
	print()


func redraw_lines_from_neuron(neuron : Node2D):
	for connection in neuron_connections:
		if connection[0] == neuron:
			connection[2].set_point_position (0, neuron.position + Vector2(grid.grid_size / 2, grid.grid_size / 2))
		elif connection[1] == neuron:
			connection[2].set_point_position (1, neuron.position + Vector2(grid.grid_size / 2, grid.grid_size / 2))
			
	
func reposition_neuron():
	if not grid.is_visible:
		return
	
	for neuron in self.neurons:
		neuron.resize_to_grid(grid.grid_size)
		neuron.position = grid.snap_to_grid(neuron)
