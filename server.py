#!/usr/bin/env python3
import numpy as np
from flask import Flask, jsonify, request

# Create an app
app = Flask(__name__)


class Bandit:
    def __init__(self, name):
        self.clks = 0
        self.views = 0
        self.name = name

    def sample(self):
        # Beta(1, 1) is the prior
        a = 1 + self.clks
        b = 1 + self.views - self.clks
        return np.random.beta(a, b)

    def add_click(self):
        self.clks += 1

    def add_view(self):
        self.views += 1

        # Print stats
        if self.views % 50 == 0:
            print(f"{self.name}: clicks: {self.clks}, views: {self.views}")


# Initialize bandits
banditA = Bandit("A")
banditB = Bandit("B")


@app.route("/get_ad")
def get_ad():
    if banditA.sample() > banditB.sample():
        ad = "A"
        banditA.add_view()
    else:
        ad = "B"
        banditB.add_view()
    return jsonify({"advertisement_id": ad})


@app.route("/click_ad", methods=["POST"])
def click_ad():
    result = "OK"
    if request.form["advertisement_id"] == "A":
        banditA.add_click()
    elif request.form["advertisement_id"] == "B":
        banditB.add_click()
    else:
        result = "Invalid Input."

    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port="8888")
