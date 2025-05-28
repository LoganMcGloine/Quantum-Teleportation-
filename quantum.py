from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_bloch_multivector
from qiskit.quantum_info import Statevector
import matplotlib.pyplot as plt

#Create a 3-qubit circuit with 3 classical bits
qc = QuantumCircuit(3, 3)

# Ask the user for the state to teleport
print("Enter the state to teleport (0, 1, or +):")
desired_state = input()

if desired_state == "1":
    qc.x(0)
elif desired_state == "+":
    qc.h(0)

# Save the original statevector to display later
initial_state = Statevector.from_instruction(qc)

#Create an entangled Bell pair between qubit 1 (Alice) and qubit 2 (Bob)
qc.h(1)       # Put qubit 1 in superposition
qc.cx(1, 2)   # Entangle qubit 1 and 2 (Bell state)



# ---At this point, Bob can take his qubit to his disired location---


#Entangele qubit 0 to 1
qc.cx(0, 1)

#Measure Alice's qubits and store in classical bits
qc.measure(0, 0)
qc.measure(1, 1)

#Conditional operations (Bob corrects based on Alice's measurements)
with qc.if_test((0, 1)):  # If first classical bit is 1
    qc.x(2)
with qc.if_test((1, 1)):  # If second classical bit is 1
    qc.z(2)

# Measure Bob's qubit
qc.measure(2, 2)



# Run the simulation with 10000 shots
sim = Aer.get_backend('aer_simulator')
qc = qc.reverse_bits()  # Qiskit uses little-endian for measurement so we reverse the bits
job = sim.run(qc, shots=10000) 
result = job.result()
counts = result.get_counts()

# Show the circuit
print("Quantum Teleportation Circuit:")
print(qc.draw())


#Display the resulting measurements with percentages
total_shots = sum(counts.values())
print("Measurement Results:")
for outcome, count in sorted(counts.items()):
    percentage = (count / total_shots) * 100
    print(f"{outcome}: {count} times ({percentage:.1f}%)")
   

# Extract just the results for Bob's qubit (qubit 2)
bob_counts = {'0': 0, '1': 0}
for outcome, count in counts.items():
    bob_bit = outcome[0]  # Rightmost bit is Bob's qubit
    bob_counts[bob_bit] += count

print("Bob's qubit (qubit 2) measurement results:")
print(bob_counts)

# A way to visualize some of the states of the qubit in a bloch sphere
plt.figure(figsize=(6, 6))
plot_bloch_multivector(initial_state.data)
plt.title("Initial State (Qubit 0)")
plt.show()




