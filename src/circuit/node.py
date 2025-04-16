from __future__ import annotations
from circuit.etiquette import Etiquette

class Node:
  """ This class represents a Node """
  
  def __init__(self, etiquette : Etiquette, next_node : Node | None = None):
    self.etiquette = etiquette
    self.next_node = next_node
    self.inputs = []
    self.output = None
    
  def set_next_node(self, next_node : Node):
    self.next_node = next_node
    
  def get_next_node(self) -> Node:
    return self.next_node
  
  def get_etiquette(self) -> Etiquette:
    return self.etiquette
  
  def get_output(self) :
    return self.output
  
  def set_output(self, value):
    self.output = value

  def get_indeg(self, edges : dict[Node, list[Node]]) -> int:
    count = 0
    for neighbors in edges.values():
        count += neighbors.count(self)
    return count
  
  def get_outdeg(self, edges : dict[Node, list[Node]]) -> int:
    return len(edges[self])
  
  def reset(self) :
    self.output = None
    self.inputs = []