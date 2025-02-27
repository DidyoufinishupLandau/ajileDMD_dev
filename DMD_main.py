from DMD_driver import DMD_driver
import numpy as np
import time
from skimage import transform
class control_DMD:
    def __init__(self, pattern, project_name: str, main_sequence_itr: int, frame_time :int=50):
        """
        Given pattern [[mask], [mask], [mask]...], control DMD
        :param pattern: 3D array or list[2D array]
        :param project_name: name of the project
        :param main_sequence_itr: iteration of main sequence. The hierarchy is main sequence( sequence(frame<->image))
        :param frame_time:time stay on one frame
        """
        self. pattern = pattern
        self.project_name = project_name
        self.main_sequence_itr = main_sequence_itr
        self.frame_time = frame_time
    def execute(self,pattern_start, pattern_end):
            dmd = DMD_driver()
            dmd.create_project(project_name=self.project_name)
            dmd.create_main_sequence(seq_rep_count=self.main_sequence_itr)

            #for j in range( 5000*(i),  ceil_num):
            for j in range(pattern_start , pattern_end):
                dmd.add_sequence_item(image=rescale(self.pattern[j]), seq_id=1, frame_time=self.frame_time)
            dmd.my_trigger()
            dmd.start_projecting()
            print("sleep:", self.frame_time/1000*1.01*(pattern_end-pattern_start))
            time.sleep(self.frame_time/1000*1.01*(pattern_end-pattern_start))
            dmd.stop_projecting()
def rescale(input_image: np.array) -> np.array:
    """
    resize any size image into 1140 * 912 image.
    :param input_image: single mask
    :return:
    2D array: single mask
    """
    rs = transform.resize(input_image, (1140, 912), order=0, anti_aliasing=False)
    return rs