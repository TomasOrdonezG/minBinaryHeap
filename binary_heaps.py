import random

class HeapNode:
  def __init__(self, key, value=None, left=None, right=None, parent=None) -> None:
    self.__key = key
    self.__value = value
    self.__left = left
    self.__right = right
    self.__parent = parent

  def __str__(self):
    parent = self.getParent()
    left = self.getLeft()
    right = self.getRight()
    return f'\nParent: {parent.getKey() if parent else parent}\Key: {self.getKey()}\nLeft: {left.getKey() if left else left}\nRight: {right.getKey() if right else right}\n'

  def __repr__(self):
    parent = self.getParent()
    parent = parent.getKey() if parent else parent
    left = self.getLeft()
    left = left.getKey() if left else left
    right = self.getRight()
    right = right.getKey() if right else right
    return f'Node: {[parent, self.getKey(), left, right]}'

  def getKey(self):
    '''Returns the key'''
    return self.__key

  def getLeft(self):
    '''Returns the left child'''
    return self.__left

  def getRight(self):
    '''Returns the right child'''
    return self.__right

  def getParent(self):
    '''Returns the parent'''
    return self.__parent
    
  def getValue(self):
    '''Returns the value'''
    return self.__value
  
  def setLeft(self, left) -> None:
    '''Sets the left child to a new Node'''
    self.__left = left
  
  def setRight(self, right) -> None:
    '''Sets the right child to a new Node'''
    self.__right = right

  def setParent(self, parent) -> None:
    '''Sets the parent to a new Node'''
    self.__parent = parent

class MinBinaryHeap:
  # * Private methods
  def __init__(self, rootKey, rootValue=None) -> None:
    rootValue = rootKey if rootValue is None else rootValue
    self.__root: HeapNode = HeapNode(rootKey, rootValue)
    self.__depth = 0
    self.__size = 1

  def __getLeadingSpaces(self, level) -> int:
    if level == 0:
      return 0
    elif level == 1:
      return 1
    else:
      return (self.__getLeadingSpaces(level-1) * 2) + 1
  
  def __getBetweenSpaces(self, level) -> int:
    if level == 0:
      return 1
    else:
      return (self.__getBetweenSpaces(level - 1) * 2) + 1

  def __str__(self, nodes=None, level=None,init=True) -> str:
    if init:
      nodes = [self.__root]
      level = self.__depth

    space = ' '
    leadingSpace = self.__getLeadingSpaces(level) * space
    betweenSpace = self.__getBetweenSpaces(level) * space
    thisLevel = leadingSpace
    children = []
    
    for node in nodes:
      if node:
        children.append(node.getLeft())
        children.append(node.getRight())
        key = str(node.getKey())
        thisLevel += key + betweenSpace

    if level == 0:
      return thisLevel
    else:
      return thisLevel + '\n' + self.__str__(nodes=children, level=level-1, init=False)

  def __addNewNode(self, key, value=None) -> HeapNode:
    newNode = HeapNode(key, value)
    
    # path to the next parent node by turning the size of the heap into a binary string, 0 is left and 1 is right
    pathToNextNode = bin(self.getSize()+1)[3:]
    pathToNextParent = pathToNextNode[:-1]
    nextNodePosition = pathToNextNode[-1]  # Child pos is the last digit of the binary string
    heapWasFull = self.isFull()  # Check if the heap is full before adding the new node
    
    # Init parent as root and follow the created path
    parent = self.__root
    for direction in pathToNextParent:
      parent = parent.getLeft() if direction == '0' else parent.getRight()
    
    # Append node and increment size
    if nextNodePosition == '0':
      parent.setLeft(newNode)
    else:
      parent.setRight(newNode)
    newNode.setParent(parent)
    self.__size += 1
    
    # Increment depth if new node was added at a new depth
    if heapWasFull:
      self.__depth += 1
    
    return newNode
  
  def __switchWithParent(self, child: HeapNode):
    assert not (child is self.__root), 'Error, can\'t switch root with its parent of type None'
    parent: HeapNode = child.getParent()
    leftChild = child is parent.getLeft()
    leftGrandchild, rightGrandchild, grandParent = child.getLeft(), child.getRight(), parent.getParent()
    if leftChild:
      hasSibling = parent.getRight() != None
      child.setLeft(parent)
      if hasSibling:
        rightSibling = parent.getRight()
        child.setRight(rightSibling)
        rightSibling.setParent(child)
    else:
      child.setRight(parent)
      leftSibling = parent.getLeft()
      child.setLeft(leftSibling)
      leftSibling.setParent(child)
    child.setParent(grandParent)
    parent.setParent(child)
    parent.setLeft(leftGrandchild)
    parent.setRight(rightGrandchild)
    if grandParent:
      parentLeftChild = parent is grandParent.getLeft()
      if parentLeftChild:
        grandParent.setLeft(child)
      else:
        grandParent.setRight(child)
    if leftGrandchild:
      leftGrandchild.setParent(parent)
      if rightGrandchild:
        rightGrandchild.setParent(parent)
  
  def __permuteNode(self, current: HeapNode):
    '''Permutes the given node to make the min heap valid
    each node is bigger than or equal to its parent'''
    
    while not (current.getParent().getKey() <= current.getKey()):  # While the parent's key is greater than the child's
      self.__switchWithParent(current)  # Switch
      if not current.getParent():
        # If the current node has no parent then it is the new root of the heap and we break out of the loop
        self.__root = current
        break
      
  def __removeRoot(self):
    path = bin(self.__size)[3:]
    oldRoot = self.__root
    newRoot = oldRoot
    for direction in path:
      if direction == '0':
        newRoot = newRoot.getLeft()
      else:
        newRoot = newRoot.getRight()
    oldParent = newRoot.getParent()
    newRootLeftChild = not oldParent.getRight()
    if newRootLeftChild:
      oldParent.setLeft(None)
    else:
      oldParent.setRight(None)
    self.__root = newRoot
    rootLeft, rootRight = oldRoot.getLeft(), oldRoot.getRight()
    oldRoot.setLeft(None)
    oldRoot.setRight(None)
    newRoot.setParent(None)
    newRoot.setLeft(rootLeft)
    newRoot.setRight(rootRight)
    if rootLeft:
      rootLeft.setParent(newRoot)
    if rootRight:
      rootRight.setParent(newRoot)
    self.__size -= 1
    if self.isFull():
      self.__depth -= 1
    
    # Check if its full to change the depth, can't use method because it depends on the depth
    num = self.getSize()+1
    while num % 2 == 0:
      num /= 2
    fullTree = num == 1
    if fullTree:
      self.__depth -= 1

    return oldRoot
  
  def __permuteRoot(self):
    current = self.__root
    done = False
    while not done:
      leftChild = current.getLeft()
      rightChild = current.getRight()
      if leftChild and rightChild:
        smallerChild = leftChild if leftChild.getKey() <= rightChild.getKey() else rightChild
      elif leftChild:
        smallerChild = leftChild
      else:
        break
      
      if current.getKey() > smallerChild.getKey():
        self.__switchWithParent(smallerChild)
        if current is self.__root:
          self.__root = smallerChild
      else:
        done = True

  # * Public methods
  def peek(self) -> HeapNode:
    '''Returs the Root of the heap as a HeapNode object'''
    return self.__root
  
  def getDepth(self) -> int:
    '''Returns the depth of the heap'''
    return self.__depth

  def getSize(self) -> int:
    '''Returns the size of the heap'''
    return self.__size

  def isFull(self) -> bool:
    '''Returns True if the heap is full, otherwise False'''
    current = self.__root
    currentDepth = 0
    while current.getRight():
      current = current.getRight()
      currentDepth += 1

    return currentDepth == self.__depth
  
  def heapPush(self, key, value=None) -> None:
    '''Pushes a new HeapNode with a key and value into the heap and updates it accordingly'''
    newNode = self.__addNewNode(key, value)
    self.__permuteNode(newNode)

  def heapPop(self) -> HeapNode:
    '''Removes and returns the root of the heap and updates it accordingly'''
    assert self.getSize() != 1, 'Error, cannot dequeue a Heap with size of 1'
    oldRoot = self.__removeRoot()
    print(self)
    self.__permuteRoot()
    return oldRoot

def main() -> None:
  randHeap = MinBinaryHeap(random.randint(1, 9))
  for _ in range(14):
    randHeap.heapPush(random.randint(1, 9))
  print(randHeap)

if __name__ == '__main__':
  main()