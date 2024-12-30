from clients.CommandsClient import CommandsClient
from utils.PropertiesReader import PropertiesReader
from inforeception.CarInformationReceptor import CarInformationReceptor
from inforeception.SelectedDataReceptor import SelectedDataReceptor
import threading
import time
import os
import uuid


class ComplexCommand360:

    number_of_steps = 20

    time_sleep_move = 0.15
    time_sleep_adjust_image = 1.5

    instance = None

    @staticmethod
    def get_instance():

        if ComplexCommand360.instance is None:
            ComplexCommand360.instance = ComplexCommand360()

        return ComplexCommand360.instance

    def __init__(self):
        self.running = False
        self.commands_client = CommandsClient.get_instance()

        properties_reader = PropertiesReader.get_instance()
        train_path = f'{properties_reader.room_dataset_path}/train'
        self.images_path = f'{train_path}/images'
        self.labels_path = f'{train_path}/labels'
        os.makedirs(self.images_path, exist_ok=True)
        os.makedirs(self.labels_path, exist_ok=True)

        room_list = properties_reader.room_list.split(",")
        self.data_yaml_path = f'{properties_reader.room_dataset_path}/data.yaml'
        if not os.path.exists(self.data_yaml_path):
            with open(self.data_yaml_path, 'w') as data_yaml_file:
                data_yaml_file.write(f'train: ../train/images\n\nnc: {len(room_list)}\nnames: {room_list}')

    def stop(self):
        self.running = False

    def execute(self):

        execution_thread = threading.Thread(target=self.execute_inner)
        execution_thread.start()

    def execute_inner(self):

        print("ComplexCommand360!!!!!!!")

        self.running = True

        for step in range(ComplexCommand360.number_of_steps):

            if not self.running:
                return

            self.move_step()
            self.save_image_in_corpus()

    def save_image_in_corpus(self):

        id_selected_room = SelectedDataReceptor.get_instance().id_selected_room
        selected_room = SelectedDataReceptor.get_instance().selected_room

        if id_selected_room is None:
            print("No selected ROOM")
            return

        uuid4 = uuid.uuid4()
        image_file_name = f'{selected_room}_{uuid4}.png'

        last_image = CarInformationReceptor.get_instance().last_image
        last_image.save(f'{self.images_path}/{image_file_name}.png')

        with open(f'{self.labels_path}/{image_file_name}.txt', 'w') as labels_file:
            labels_file.write(f'{id_selected_room} 0.5 0.5 1 1\n')

    def move_step(self):

        self.commands_client.move_turn_left()
        time.sleep(ComplexCommand360.time_sleep_move)
        self.commands_client.move_stop()
        time.sleep(ComplexCommand360.time_sleep_adjust_image)

