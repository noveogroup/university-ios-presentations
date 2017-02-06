#generate index
python CreateLecture.py -s source/docs/index.md -t source/templates/lecture_X.html -e source/engine -d source/ 

#generate lections
for i in source/docs/lecture*.md; do
    python CreateLecture.py -s $i -t source/templates/lecture_X.html -e source/engine -d source/docs
done