from __future__ import annotations
from src.circuit.etiquette import Etiquette

class Node:
  """ This class represents a Node with a tag for the type of logic gate """

  def __init__(self, etiquette : Etiquette):
    self.etiquette = etiquette
    self.output = None

  def get_etiquette(self) -> Etiquette:
    """ Return the tag of the node """
    return self.etiquette

  def get_output(self) :
    """ Return the output value of the node """
    return self.output

  def set_output(self, value):
    """ Change the ouput value of the node """
    self.output = value

  def get_indeg(self, reverse_edges : dict[Node, list[Node]]) -> int:
    """ return the number of nodes before """
    return len(reverse_edges[self])

  def get_outdeg(self, edges : dict[Node, list[Node]]) -> int:
    """ return the number of nodes after """
    return len(edges[self])

  def reset(self) :
    """ Reset the value of the output """
    self.output = None