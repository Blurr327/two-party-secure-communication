from __future__ import annotations
from circuit_combinatoire import Etiquette
from utils.binary import bit

class Node:
  """sumary_line
  
  Keyword arguments:
  argument -- description
  Return: return_description
  """
  
  def __init__(self, value, next_node : Node | None = None):
    self.value = value
    self.next_node = next_node
    
  def set_next_node(self, next_node : Node):
    self.next_node = next_node
    
  def get_next_node(self) -> Node:
    return self.next_node
  
  def get_value(self) :
    return self.value
  
  def get_indeg(self, edges : list[tuple[Node, Node]]) -> int:
    indeg = 0
    for edge in edges:
      if edge[1] == self:
        indeg += 1
    return indeg
  
  def get_outdeg(self, edges : list[tuple[Node, Node]]) -> int:
    outdeg = 0
    for edge in edges:
      if edge[0] == self:
        outdeg += 1
    return outdeg