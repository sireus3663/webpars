import sys
sys.dont_write_bytecode = True #чтобы пайкесш не создавался пока

from terminal.init import Terminal


config = Terminal().run()
print(config)
