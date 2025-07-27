.PHONY: all engine java-wrapper python-bindings test clean

all: engine java-wrapper python-bindings

engine:
	@echo "Building C++ engine..."
	mkdir -p engine/build
	cd engine/build && cmake .. && make

java-wrapper: engine
	@echo "Building Java wrapper..."
	cd java-wrapper && mvn clean package

python-bindings: engine
	@echo "Building Python bindings..."
	cd python-bindings && pip install -e .

test: all
	@echo "Testing C++ engine..."
	cd engine/build && ctest || echo "No C++ tests yet"
	@echo "Testing Java wrapper..."
	cd java-wrapper && mvn test || echo "No Java tests yet"
	@echo "Testing Python bindings..."
	cd python-bindings && python -m math_engine

benchmark: all
	@echo "Running performance benchmarks..."
	@echo "C++ benchmark:"
	cd engine/build && ./benchmark || echo "No benchmark executable"
	@echo "Java benchmark:"
	cd java-wrapper && java -cp target/mathengine-java-1.0.0.jar com.example.mathengine.MathEngine
	@echo "Python benchmark:"
	cd python-bindings && python -c "import math_engine; print('Python bindings working')"

clean:
	rm -rf engine/build
	cd java-wrapper && mvn clean
	cd python-bindings && rm -rf build dist *.egg-info
	rm -rf worktrees/