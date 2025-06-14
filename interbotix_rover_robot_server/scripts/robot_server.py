#!/usr/bin/env python
import grpc
import rospy
from concurrent import futures
from interbotix_rover_robot_server.ros_bridge import InterbotixRoverRosBridge
from robo_gym_server_modules.robot_server.grpc_msgs.python import robot_server_pb2, robot_server_pb2_grpc

class RobotServerServicer(robot_server_pb2_grpc.RobotServerServicer):
    def __init__(self, real_robot, robot_model):
        self.rosbridge = InterbotixRoverRosBridge(real_robot=real_robot, robot_model=robot_model)

    def GetState(self, request, context):
        try:
            return self.rosbridge.get_state()
        except:
            rospy.logerr('Failed to get state', exc_info=True)
            return robot_server_pb2.State(success=0)

    def SetState(self, request, context):
        try:
            self.rosbridge.set_state(state_msg=request)
            return robot_server_pb2.Success(success=1)
        except:
            rospy.logerr('Failed to set state', exc_info=True)
            return robot_server_pb2.Success(success=0)

    def SendAction(self, request, context):
        try:
            executed_action = self.rosbridge.send_action(request.action)
            return robot_server_pb2.Success(success=1)
        except:
            rospy.logerr('Failed to send action', exc_info=True)
            return robot_server_pb2.Success(success=0)

    def SendActionGetState(self, request, context):
        try:
            executed_action = self.rosbridge.send_action(request.action)
            return self.rosbridge.get_state()
        except:
            rospy.logerr('Failed to send action and get state', exc_info=True)
            return robot_server_pb2.State(success=0)


def serve():
    rospy.loginfo('Starting Interbotix Rover Robot Server...')
    server_port = rospy.get_param('~server_port')
    real_robot = rospy.get_param('~real_robot')
    robot_model = rospy.get_param('~robot_model')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    robot_server_pb2_grpc.add_RobotServerServicer_to_server(
        RobotServerServicer(real_robot=real_robot, robot_model=robot_model), server)
    server.add_insecure_port('[::]:'+repr(server_port))
    server.start()
    if real_robot:
        rospy.loginfo(robot_model + ' Real Robot Server started at ' + repr(server_port))
    else:
        rospy.loginfo(robot_model + ' Sim Robot Server started at ' + repr(server_port))
    rospy.spin()


if __name__ == '__main__':
    try:
        wait_time = 5
        rospy.init_node('robot_server')
        rospy.loginfo('Waiting {}s before starting initialization of Robot Server'.format(wait_time))
        rospy.sleep(wait_time)
        serve()
    except (KeyboardInterrupt, SystemExit):
        pass