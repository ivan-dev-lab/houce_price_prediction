<h1> house_price_prediction </h1>
<hr>
<p>Модель решает задачи регрессии, в частности - предсказание цен на недвижимость</p>
<p>Модель создана в учебных целях для освоения методов машинного обучения.</p>
<p>В ходе проекта также были проанализированы цены на недвижимость в Сведловской области</p>
<h2>Установка и использование</h2>
<ol>
<li>Убедитесь, что у вас установлена последняя версия Python и инструмент управления пакетами pip.
<code>Windows</code>+<code>R</code>-><code>cmd</code>
<br><br>
<code>python --version</code>
<br><br>
<code>pip --version</code>
</li>
<br>
<li>Клонирование репозитория:<br>
<code>Windows</code>+<code>R</code>-><code>cmd</code>
<br><br>
Переход в директорию, где будет хранится исходный код:<br>
<code>cd YOUR_DIRECTORY</code>
<br><br>
Клонирование исходного кода в выбранную директорию:<br>
<code>git clone https://github.com/ivan-dev-lab/houce_price_prediction.git</code>
<br><br>
Установка необходимых библиотек:<br>
<code>pip install -r requirements.txt</code></li>
<br>
<li>Для отображения результатов обучения:
<br>
<code>cd YOUR_DIRECTORY</code>
<br><br>
<code>python main.py</code></li>
</ol>
<h2>Примеры использования:</h2>
<p>Как уже было написано, модель была выполнена исключительно в учебных целях для изучения методов машинного обучения, следовательно не может быть использована в практических задачах из-за специфики данных ( данные по недвижимости ориентированы на Австралию )</p>
<h2>Данные:</h2>
<ol>
<li>Данные, взятые с сайта <b><a href="https://www.kaggle.com/datasets/shree1992/housedata?select=data.csv">kaggle.com</a></b> находятся в <code>YOUR_DIRECTORY/data/houses-data_kaggle.csv</code> </li>
<li>Данные, взятые с сайта <b><a href="https://dom.mirkvartir.ru/%D0%A1%D0%B2%D0%B5%D1%80%D0%B4%D0%BB%D0%BE%D0%B2%D1%81%D0%BA%D0%B0%D1%8F+%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C/%D0%97%D0%B0%D0%B3%D0%BE%D1%80%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F+%D0%BD%D0%B5%D0%B4%D0%B2%D0%B8%D0%B6%D0%B8%D0%BC%D0%BE%D1%81%D1%82%D1%8C/">https://dom.mirkvartir.ru/</a></b> находятся в <code>YOUR_DIRECTORY/house_review/houses-data.csv</code> </li>
</ol>
<h2>Архитектура модели:</h2>
<p>После списка представлен исходный код архитектуры модели ( находится в <code>YOUR_DIRECTORY/create_model.py</code> )</p>
<ol>
<li>Тип модели: <code>keras.models.Sequential()</code> - информация от одного слоя модели к другому идет последовательно</li>
<br>
<li><b>Слои:</b>
    <p>Во всех слоях ( кроме выходного ) используется функция активации <b>ReLU</b>.</p>
    <ul>
        <li><b>Input Layer</b>: Входной слой, принимающий признаки.<br>Количество нейронов = <b>100</b>.<br>Размерность входных данных = <b>(55, )</b> </li>
        <li><b>Dropout Layer 1</b>: Слой используется как метод регуляризации для первого полносвязного слоя.<br>Коэффицент выпадения = <b>0.5</b></li>
        <li><b>Dense Layer 2</b>: Второй полносвязный слой.<br>Количество нейронов = <b>100</b>.<br>Используется регуляризатор <code>l1</code> с фактором = <b>0.01</b></li>
        <li><b>Dense Layer 3</b>: Третий полносвязный слой.<br>Количество нейронов = <b>50</b>.<br>Используется регуляризатор <code>l2</code> с фактором = <b>0.01</b></li>
        <li><b>Output Layer</b>: Выходной слой, использутся для получения целевой переменной.<br>Количество нейронов = <b>1</b>.</li>
    </ul>
</li>
<li>При компиляции модели используются:
<ul>
    <li>Функция-оптимизатор: <code>RMSprop</code> со скоростью обучения = <b>0.01</b></li>
    <li>Функция потерь: <code>Mean-Squared-Error</code></li>
    <li>Метрики: <code>[MeanSquaredError()]</code></li>
</ul>
</li>
<br>
<p>Исходный код архитектуры модели:</p>

<code>model = Sequential()</code><br>
<code>model.add(layer=Dense(units=100, activation="relu", input_shape=(input_shape,)))</code><br>
<code>model.add(layer=Dropout(0.5))</code><br>
<code>model.add(layer=Dense(units=100, activation="relu", kernel_regularizer=regularizers.l1(0.01)))</code><br>
<code>model.add(layer=Dense(units=50, activation="relu", kernel_regularizer=regularizers.l2(0.01)))</code><br>
<code>model.add(layer=Dense(units=1))</code><br>

<code>model.compile(optimizer=RMSprop(learning_rate= 0.01), loss="mse", metrics=[MeanSquaredError()])</code>

</ol>
<h2>Итоговые результаты модели:</h2>
<code>mse = <b>43718843934.33928</b></code><br>
<code>mae = <b>114910.8332076866</b></code><br>
<code>r2_score = <b>0.706132088973525</b></code>

<p>В целях улучшения точности модели и снижения mse и mae сделан фокус на улучшение имеющихся данных</p>
<h2>Автор проекта</h2>
<p>Улановский Иван:</p>
<ol>
<li><a href="https://github.com/ivan-dev-lab">GitHub</a></li>
<li><a href="https://t.me/ivan_ne_chik06">Telegram</a></li>
</ol>