import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from dynamicProjectileMotion.plotting import interactive_plot

def main():
    interactive_plot()

if __name__ == "__main__":
    main()
