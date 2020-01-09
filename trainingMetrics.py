import matplotlib.pyplot as plt
import numpy as np
import os.path


def calculate_regression_line(episodes, rewards):
    slope = (((np.mean(episodes) * np.mean(rewards)) - np.mean(episodes * rewards)) /
         ((np.mean(episodes) * np.mean(episodes)) - np.mean(episodes * episodes)))
    intercept = np.mean(rewards) - slope * np.mean(episodes)
    regression_line = (slope * episodes) + intercept
    return regression_line


def plot_reward(training_history):
    session_reward = np.array(training_history.history['episode_reward'])
    session_episodes = np.arange(session_reward.size)

    if os.path.exists('reward_history.npy'):
        overall_reward = np.load('reward_history.npy')
        overall_reward = np.concatenate((overall_reward, session_reward))
    np.save('reward_history.npy', overall_reward)  # save

    session_regression_line = calculate_regression_line(session_episodes, session_reward)
    plt.scatter(session_episodes, session_reward)
    plt.plot(session_episodes, session_regression_line)
    plt.title('training session results')
    plt.ylabel('episode reward')
    plt.show()

    overall_episodes = np.arange(overall_reward.size)
    overall_regression_line = calculate_regression_line(overall_episodes, overall_reward)
    plt.scatter(overall_episodes, overall_reward)
    plt.plot(overall_episodes, overall_regression_line)
    plt.title('overall training results')
    plt.ylabel('episode reward')
    plt.show()


def plot_wins():
    if os.path.exists('win_history.npy'):
        win_history = np.load('win_history.npy')
        matches = np.arange(win_history.size)
        regression_line = calculate_regression_line(matches, win_history)

        plt.scatter(matches, win_history)
        plt.plot(matches, regression_line)
        plt.yticks([1.0, 0.0], ["True",
                                "False"])
        plt.title('training results')
        plt.ylabel('win')
        plt.xlabel('match number')
        plt.text(0, 0.5, "Win percentile: {}%".format(100*sum(win_history)/win_history.size))
        plt.show()


def save_wins(player_win):
    if os.path.exists('win_history.npy'):
        win_history = np.load('win_history.npy')
        win_history = np.concatenate((win_history, [player_win]))
    else:
        win_history = [player_win]
    np.save('win_history.npy', win_history)