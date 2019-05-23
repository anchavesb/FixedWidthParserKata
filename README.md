# Data Engineering Coding Challenge

#### How to build it:
~~~
docker build . --tag=latitude:latest

~~~

#### How to run it:
1. Create a directory with the required files (spec, input_file)
~~~
 ls ~/temp/files/
spec.json  test.txt
~~~

2. Run the docker image, mounting the directory as a volume
~~~
andres@bernard:~/repos/misc/data-code-kata$ docker run -it --rm latitude:latest python3 src/main.py -h
usage: main.py [-h] --spec_json SPEC_JSON --input_file INPUT_FILE
               --output_file OUTPUT_FILE [--output_delimiter OUTPUT_DELIMITER]

optional arguments:
  -h, --help            show this help message and exit
  --spec_json SPEC_JSON
                        JSON Spec
  --input_file INPUT_FILE
                        Fixed width file
  --output_file OUTPUT_FILE
                        Fixed width file
  --output_delimiter OUTPUT_DELIMITER
                        Delimiter
~~~
~~~
docker run -it -v ~/temp/files:/files --rm latitude:latest python3 src/main.py\
 --input_file /files/test.txt \
 --output_file /files/output.txt \
 --spec_json /files/spec.json
~~~

3. Check the output file
~~~
ls ~/temp/files/output.txt 
/home/andres/temp/files/output.txt
~~~


#### How to run the unit tests
~~~
docker run -it -v ~/temp/files:/files --rm latitude:latest python3 test/test_parser.py
~~~
