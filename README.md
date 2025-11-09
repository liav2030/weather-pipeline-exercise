המערכת דוגמת את מזג האוויר בזמן אמת מה api של openweather מעבדת את הנתונים ושולחת אותם לRabbitMQ.
משם logstash צורך את הנתונים כ consumer ומזרים אותם לelasticsearch שהוא משמש כ datasource של grafana.
בנוסף נבנה cicd מלא משולב runners hosted and self-hosted לצורך בנייה קלה ומהירה בrunner מנוהל ופריסה על המחשב האישי שלי.


collector-
תוכנית שדוגמת את ה־API של OpenWeather כל שעה , ושולחת הודעות JSON ל־RabbitMQ.