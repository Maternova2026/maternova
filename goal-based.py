
class Metric:
    def __init__(self, name, calculation):
        self.name = name
        self.calculation = calculation  # function

    def evaluate(self, data):
        return self.calculation(data)


class Question:
    def __init__(self, text):
        self.text = text
        self.metrics = []

    def add_metric(self, metric):
        self.metrics.append(metric)

    def evaluate(self, data):
        results = {}
        for metric in self.metrics:
            results[metric.name] = metric.evaluate(data)
        return results


class Goal:
    def __init__(self, description):
        self.description = description
        self.questions = []

    def add_question(self, question):
        self.questions.append(question)

    def evaluate(self, data):
        results = {}
        for question in self.questions:
            results[question.text] = question.evaluate(data)
        return results



data = {
    "total_patients": 120,
    "attended_appointments": 90,
    "missed_appointments": 30,
    "complications_reported": 10,
    "successful_deliveries": 100
}


# Define Metrics


attendance_rate = Metric(
    "Attendance Rate (%)",
    lambda d: (d["attended_appointments"] / d["total_patients"]) * 100
)

missed_rate = Metric(
    "Missed Appointment Rate (%)",
    lambda d: (d["missed_appointments"] / d["total_patients"]) * 100
)

complication_rate = Metric(
    "Complication Rate (%)",
    lambda d: (d["complications_reported"] / d["total_patients"]) * 100
)

success_rate = Metric(
    "Delivery Success Rate (%)",
    lambda d: (d["successful_deliveries"] / d["total_patients"]) * 100
)


# Define Questions


q1 = Question("How many patients attend antenatal appointments?")
q1.add_metric(attendance_rate)
q1.add_metric(missed_rate)

q2 = Question("What is the quality of maternal care?")
q2.add_metric(complication_rate)
q2.add_metric(success_rate)


# Define Goal


goal = Goal("Improve maternal healthcare quality and monitoring")
goal.add_question(q1)
goal.add_question(q2)


# Evaluate System


results = goal.evaluate(data)

# Display results
print("=== GQM Evaluation Results ===")
for question, metrics in results.items():
    print(f"\nQuestion: {question}")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.2f}%")