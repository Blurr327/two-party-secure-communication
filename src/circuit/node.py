from __future__ import annotations

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
  
  def get_indeg(self, edges : dict[Node, list[Node]]) -> int:
    count = 0
    for neighbors in edges.values():
        count += neighbors.count(self)
    return count
  
  def get_outdeg(self, edges : dict[Node, list[Node]]) -> int:
    return len(edges[self])