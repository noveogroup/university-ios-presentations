#generate index
python CreateLecture.py -s source/index.md -t templates/lecture_X.html

#generate lections
for i in source/*.md; do
    python CreateLecture.py -s $i -t templates/lecture_X.html -d html
done