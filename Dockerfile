FROM python:3.6

COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000

ENV SECRET_KEY=2dc56*4+14n5f@%wbnw2z6@oatcdq$zd8(l+v^nz8-nfadlstq
ENV DEBUG=1
ENV SUPERUSERNAME=admin
ENV SUPERUSEREMAIL=al.ol.chistyakov@gmail.com
ENV SUPERUSERPASSWORD=password

WORKDIR mwp_task
RUN python3 manage.py migrate
RUN echo "from django.contrib.auth.models import User; User.objects.create_superuser('$SUPERUSERNAME', '$SUPERUSEREMAIL', '$SUPERUSERPASSWORD')" | python manage.py shell
CMD python3 manage.py runserver 0.0.0.0:8000