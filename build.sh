#generate index
python CreateLecture.py -s docs/index.md -t templates/lecture_X.html -e engine

#generate lections
for i in docs/lecture*.md; do
    python CreateLecture.py -s $i -t templates/lecture_X.html -e engine -d docs
done