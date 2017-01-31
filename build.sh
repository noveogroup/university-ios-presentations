#generate lections
python CreateLecture.py -s source/index.md -t templates/lecture_X.html
python CreateLecture.py -s source/lecture_1.md -t templates/lecture_X.html -d html
python CreateLecture.py -s source/lecture_2.md -t templates/lecture_X.html -d html
python CreateLecture.py -s source/lecture_3.md -t templates/lecture_X.html -d html
python CreateLecture.py -s source/lecture_4.md -t templates/lecture_X.html -d html
python CreateLecture.py -s source/lecture_5_1.md -t templates/lecture_X.html -d html
python CreateLecture.py -s source/lecture_5_2.md -t templates/lecture_X.html -d html
python CreateLecture.py -s source/lecture_6.md -t templates/lecture_X.html -d html
python CreateLecture.py -s source/lecture_7.md -t templates/lecture_X.html -d html
python CreateLecture.py -s source/lecture_8.md -t templates/lecture_X.html -d html
python CreateLecture.py -s source/lecture_9.md -t templates/lecture_X.html -d html
python CreateLecture.py -s source/lecture_10.md -t templates/lecture_X.html -d html
python CreateLecture.py -s source/lecture_11.md -t templates/lecture_X.html -d html

#copy resources
mkdir public
cp -r engine public/
cp -r source public/
cp -r html public/
cp index.html public/
