# pySimpleNLG<br/>
**A python port of SimpleNLG**

This project is a direct port of the java code **[SimpleNLG v4.4.8 (released on Apr 10, 2016)](https://github.com/simplenlg/simplenlg)** to python.  The port replicates (almost) all the classes and methods in the java API identically.

## Documentation and Usage
The original project has a wiki tutorial and numerous examples on how to use the code.  Since the API remains same, all of those examples are still valid and provide a great place to start.  In addition, the test directory here has a large number of test cases you can use as examples.

The original java code has excellent javadoc documentation available **[here](https://github.com/simplenlg/simplenlg/tree/v4.4.8/docs/javadoc)**.  Simply download a local copy and open *index.html* in your browser to view.  The code comments were not ported into python so please use the original documentation.


## Compatibility and Setup
The project is compatible with python version 3.4+.  It will not work with python v2.x due to a few 3.x specific classes such as *Enum*.  The code was built and tested under Ubuntu but should be compatible with Mac or Windows.

You don't need to install any additional libraries to run the code or execute the unit tests.

To install the code with pip do..
```
pip3 install simplenlg
```

## Code Status
A few less commonly used components have been omitted.  These include:
* Sentence "aggregation" components
* The "xmlrealiser"(s)
* The java server
* The NIHDBLexicon and MultipleLexicon classes

All implemented components are fully functional.  The original project included about 175 unit-tests, all of which have been ported and pass in python.

The java code for SimpleNLG is not really that simple.  It has large if/else statements, regex and other complexities that presented a number of opportunities for errors to creep in during the port.  If you find a bug and are willing to fix it please do the following...
* Verify the correct behavior in the original java code.
* Identify the required python code changes needed to fix the issue so the behavior is the same as in java.
* Write a unit test under tests/misc to cover the changes.
* Use the provided script to run all unit tests and verify there is no adverse impact to other portions of the code.
* Submit a Pull Request (PR) here to merge the changes into the main codebase.
