import cv2
import numpy as np

def ImageToBlackList(mat):
  list = []
  for i in range(len(mat)):
    for j in range(len(mat[0])):
      if mat[i][j] == 0:
        list.append((i, j))
  return list

def ImageBlocky(arr, blocksize):
  grid = [[0 for i in range(len(arr[0]) // blocksize + 1)] for j in range(len(arr) // blocksize + 1)]
  for i in range(0, len(arr), blocksize):
    for j in range(0, len(arr[0]), blocksize):
      ink = 255
      for k in range(i, min(i + blocksize,len(arr))):
        for l in range(j, min(j + blocksize,len(arr))):
          if arr[k][l] == 0:
            ink = 0
      grid[i // blocksize][j // blocksize] = ink
  return grid
          
#jdef GridToImage(grid):
#  Mat m(len(grid[0]), len(grid), CV_32SC1, grid)
#  return m
