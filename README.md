# single2multi_robot_bag

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
