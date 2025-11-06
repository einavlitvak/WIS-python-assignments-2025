Safe sound is a prototype for a program where the user can input different sounds, combine them and know if these sounds (individual or summed) might be dangerous for humans, dogs or cats. 

I used Claude Sonnet 4 in Copliot in VSC

## Prompt 1

Write a python program that a user can input a couple or more sine waves (sin(x)) where the input are parameters that might modify the function. so amplitude as a multiplier of x and shift as a number that sums with x., and separately the lenght of each function. the program should combine them and then let the use know if the 'sound' created is dangerous for humans, dogs and/or cats based on the species threshold

## Prompt 2
Now make two new files that do the exact same thing but the user input is done differently: one that is a GUI and one that the user writes it in the command line where the order is always amplitude, frequency, shift, seconds, one wave after the other.
DO NOT CHANGE ANYTHING ELSE BESIDES THE USER INPUT AND THE STYLE FOR THE GUI
