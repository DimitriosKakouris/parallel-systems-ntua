# Parallel Computing Course 
## Academic Year 2023-24 | NTUA

### A short summary
This repository explores parallel computing paradigms through practical implementations completed as part of the Parallel Systems curriculum at the National Technical University of Athens. The work spans fundamental parallel/distributed computing architectures: shared memory systems, GPU accelerators, and distributed computing environments.

---

## Module 1: Introduction to OpenMP

### **Project: Conway's Cellular Automaton**
The first module is the classic Game of Life simulation with OpenMP parallelization.
The main aspects of the project include:
- Multi-threaded implementation with dynamic thread allocation
- Systematic performance benchmarking
- Visual representation of the result using charts.
- Execution time analysis

---

## Module 2: Shared Memory Architecture Deep Dive

### **Implementation A: Parallel K-means Classification**
Explored two distinct parallelization strategies for the clustering algorithm:
- **Strategy 1:** Synchronized shared cluster approach leveraging OpenMP directives like ```#pragma omp parallel for``` for parallel calculation of ```NewCluster``` and ```NewClusterSize```
- **Strategy 2:** Replication-based design with reduction and final calculation assigned to thread 0 (main thread).

Also explored thread affinity configurations ```GOMP_CPU_AFFINITY``` that binds threads to specific cores, cache coherence challenges, and memory locality optimizations through NUMA-aware strategies.

### **Implementation B: Synchronization Primitive Comparison**
Conducted an empirical study of locking mechanisms:
- Typical implementations: pthread mutexes ```pthread_mutex_lock``` and spinlocks ```pthread_spin_lock```
- Custom solutions: test-and-set (```tas_lock```), test-and-test-and-set (```ttas_lock```), array-based locks (```array_lock```), CLH queue locks (```clh_lock```)
- Comparative analysis with OpenMP's directives ```#pragma omp critical``` and ```#pragma omp atomic```

### **Implementation C: Floyd-Warshall Algorithm task-parallelization**
- OpenMP task decomposition of the recursive formulation
- Performance profiling across various graph dimensions
- Extended analysis comparing tiled and recursive approaches (additional work)

### **Implementation D: Thread-Safe Data Structure Design**
Investigated concurrent linked list implementations through multiple synchronization paradigms:
- Global locking approach
- Per-node locking strategy
- Optimistic concurrency control
- Deferred synchronization techniques
- Lock-free implementation

---

## Module 3: GPU Computing with CUDA

### **Advanced K-means on Graphics Processors**
Progressively refined GPU implementations demonstrating optimization techniques:

1. **Naive version:** Direct kernel implementation for cluster assignment
2. **Transpose version:** Data transposition for coalesced access patterns
3. **Shared-memory version:** Shared memory utilization for bandwidth reduction
4. **Full-offload version:** The implementation is entirely executed in GPU thus eliminating CPU-GPU transfer overhead


---

## Module 4: Distributed Computing with Message Passing (MPI)

### **Distributed K-means Implementation**
Developed a message-passing variant using MPI infrastructure:
- Inter-process communication design for cluster updates
- Scalability comparison with shared-memory OpenMP implementation

### **Parallel PDE Solver: Heat Equation**
Distributed implementation of iterative solvers for 2D thermal diffusion:
- **Method 1:** Standard Jacobi iteration
- **Method 2:** Successive over-relaxation (Gauss-Seidel variant)
- **Method 3:** Red-Black ordering SOR

Visual representation encompassed both fixed-iteration and convergence-based termination criteria, with scalability analysis across process counts.

---

This hands-on experience bridged theoretical concepts with real-world parallel computing challenges, establishing a solid foundation in modern high-performance computing techniques. Utilizing all current frameworks and libraries like CUDA, OpenMP, MPI.
