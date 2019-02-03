from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
import time
from sklearn.model_selection import cross_val_score

trainDataSet = pd.read_csv("../../cs4641/isilva3/happy.csv", sep=',', header = None, low_memory=False)

traindata = pd.get_dummies(trainDataSet)

X = trainDataSet.values[1:, 2:]
Y = trainDataSet.values[1:,0:1]

# start timer
t0 = time.clock()

cv = train_test_split(X, Y, test_size=.30)
train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size=.3)


# start timer
training_accuracy = []
validation_accuracy = []
test_accuracy = []


# For the neural network, experiment on different number of hidden layers
# Define the classifier
num_runs = 1
num_layers = 25
for layer_num in range(15):
    train_acc = 0
    cv = 0
    test_acc = 0
    print("Beginning", layer_num, "layers")
    for _ in range(num_runs):
        hiddens = [16]*layer_num
        clf = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=hiddens, random_state=1)
        clf.fit(train_x, train_y)

        train_acc += accuracy_score(train_y, clf.predict(train_x))
        cv += cross_val_score(clf, train_x, train_y, cv=7).mean()
        test_acc += accuracy_score(test_y, clf.predict(test_x))
    train_acc /= num_runs
    cv /= num_runs
    test_acc /= num_runs
    training_accuracy.append(train_acc)
    test_accuracy.append(test_acc)
    validation_accuracy.append(cv.mean())

plt.plot(training_accuracy, color='red', marker='s', label='Train Acc')
plt.plot(test_accuracy, color='blue', marker='o', label='Test Acc')
plt.plot(validation_accuracy, color='black', marker='+', label='Cross-Validation')
plt.show()