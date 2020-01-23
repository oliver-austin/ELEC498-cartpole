import sys
# sys.path.append("O:\Oliver\Anaconda\envs\gym\Lib\site-packages")
import retro
import h5py
from CNNProcessor import CNNProcessor
from InfoCallback import InfoCallback
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D, Dropout
from keras.optimizers import Adam
import os.path
from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory
from trainingMetrics import plot_reward, plot_wins, STATE_NAME

ENV_NAME = 'StreetFighterIISpecialChampionEdition-Genesis'
STATE_NAME = 'ryu1.state'

def main():
    env = retro.make(game=ENV_NAME, state=STATE_NAME, use_restricted_actions=retro.Actions.DISCRETE)
    nb_actions = env.action_space.n

    model = Sequential()
    # Conv1 32 32 (3) => 30 30 (32)
    # model.add(Conv2D(32, (3, 3), input_shape=X_shape[1:]))
    model.add(Conv2D(32, kernel_size=(8, 8), strides=4, activation="relu", input_shape=(1,) + (128, 100), data_format='channels_first'))
    model.add(Activation('relu'))
    # Conv2 30 30 (32) => 28 28 (32)
    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    # Pool1 28 28 (32) => 14 14 (32)
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    # Conv3 14 14 (32) => 12 12 (64)
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    # Conv4 12 12 (64) => 6 6 (64)
    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    # Pool2 6 6 (64) => 3 3 (64)
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    # FC layers 3 3 (64) => 576
    model.add(Flatten())
    # Dense1 576 => 256
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(128))
    model.add(Activation('relu'))
    # Dense2 256 => 10
    model.add(Dense(nb_actions))
    model.add(Activation('softmax'))

    # number of steps? and policy used for learning
    memory = SequentialMemory(limit=50000, window_length=1)
    policy = BoltzmannQPolicy()


    '''
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(8, 8), strides=4, activation="relu", input_shape=(1,) + (128, 100), data_format='channels_first'))
    model.add(Conv2D(64, kernel_size=(4, 4), strides=2, activation="relu"))
    model.add(Conv2D(64, (3, 3), activation="relu"))
    model.add(Flatten())
    model.add(Dense(512, activation="relu"))
    model.add(Dense(nb_actions))
    model.add(Activation('linear'))
    memory = SequentialMemory(limit=50000, window_length=1)
    policy = BoltzmannQPolicy()
    '''
    # print(env.observation_space)

    # Uncomment the following line to load the model weights from file
    if os.path.exists('dqn_cnn_{}_weights.h5f'.format(STATE_NAME)):
        model.load_weights('dqn_cnn_{}_weights.h5f'.format(STATE_NAME))
    dqn = DQNAgent(processor=CNNProcessor(), model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10000,
               target_model_update=1e-3, policy=policy)
    dqn.compile(Adam(lr=1e-3), metrics=['mae'])

    dqn.fit(env, nb_steps=1000000, visualize=True, verbose=2, callbacks=[InfoCallback()], action_repetition=4)
    dqn.save_weights('dqn_cnn_{}_weights.h5f'.format(STATE_NAME), overwrite=True)
    plot_wins()
    #plot_reward(training_history)

    # Uncomment the following line to overwrite the model weights file after training

    dqn.test(env, nb_episodes=5, visualize=True)


if __name__ == "__main__":
    main()