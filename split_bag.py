import argparse
import glob
import os
from fnmatch import fnmatchcase
from rosbag import Bag
from tqdm import tqdm



if __name__ == '__main__':
    # create an argument parser to read arguments from the command line
    PARSER = argparse.ArgumentParser(description=__doc__)
    # add an argument for the output bag to create
    PARSER.add_argument('--output_bag', '-o',
        type=str,
        help='The output bag file to write to',
    )
    # add an argument for the sequence of input bags
    PARSER.add_argument('--input_bags', '-i',
        type=str,
        nargs='+',
        help='A list of input bag files',
    )

    PARSER.add_argument('--split_places', '-s',
        type=int,
        nargs='+',
        help='A list of split times, relative to timestamp 0, the final timestamp must be included')

    PARSER.add_argument('--topics', '-t',
        type=str,
        nargs='*',
        help='A sequence of topics to include from the input bags.',
        default=['*'],
        required=False,
    )
    PARSER.add_argument('--robot_names', '-r',
        type=str,
        nargs='*',
        help='A sequence of robot names for various robots.',
        default=['*'],
        required=False,
    )
    # robot_names = ['/jackal0', '/jackal1', '/jackal2', '/jackal3']
    try:
        # get the arguments from the argument parser
        ARGS = PARSER.parse_args()
        # open the output bag in an automatically closing context
        topics = ARGS.topics
        split_places = ARGS.split_places
        robot_names = ARGS.robot_names
        
        cnt = 0
        time_initial = 0
        split_before = 0
        time_final = split_places[-1]
        
        with Bag(ARGS.output_bag, 'w') as output_bag:
            for filename in ARGS.input_bags:
                # for filename in glob.glob(os.path.join(foldername, '*.bag')):
                for i, [topic, msg, t] in enumerate(Bag(filename)):
                    #define initial time
                    if i == 0 and time_initial == 0:
                        time_initial = t.secs
                        split_before = 0
                        time_final = time_final + t.secs
                    elif t.secs > time_final:
                        break


                    if t.secs > split_places[cnt] + time_initial:
                        split_before = split_places[cnt]
                        cnt = cnt + 1
                        
                    #check topic filter
                    if any(fnmatchcase(topic, pattern) for pattern in topics):
                        topic = robot_names[cnt] + topic
                        # print(topic)
                        t.secs = t.secs - split_before
                        
                        # if msg._type == "sensor_msgs/PointCloud2":
                        msg.header.stamp.secs = t.secs
                        msg.header.stamp.nsecs = t.nsecs
                            # print(t.secs)
                            # print(t.nsecs)
                        output_bag.write(topic, msg, t)

 
    except KeyboardInterrupt:
        passss

                   
