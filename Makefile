drone_test: main.cpp Drone.cpp
	g++ -std=c++1z -O3 main.cpp Drone.cpp -o drone_test

clean:
	rm -rf drone test *.dylib *.so

bindings:
	c++ -I /users/nameerhirschkind/CLionProjects/DroneSim/eigen-3.3.7/ -undefined dynamic_lookup -O3 -Wall -shared -std=c++11 -fPIC `python -m pybind11 --includes` bindings.cpp Drone.cpp -o drone`python3-config --extension-suffix`

test-bindings:
	c++ -I /users/nameerhirschkind/CLionProjects/DroneSim/eigen-3.3.7/ -undefined dynamic_lookup -O3 -Wall -shared -std=c++11 -fPIC `python -m pybind11 --includes` test_bindings.cpp -o test`python3-config --extension-suffix`
