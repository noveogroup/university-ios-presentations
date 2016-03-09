				<section data-markdown><script type="text/template">
# 8. Работа с сетью

### Noveo University — iOS

#### Александр Горбунов
				</script></section>
				
				
				
				<section data-markdown><script type="text/template">
## План на сегодня

- Работа с сетью в iOS
- Загрузка в NSData
- NSURLConnection, NSURLSession
- JSON
- AFNetworking
- Демонстрация
				</script></section>



				<section data-markdown><script type="text/template">
## Работа с сетью в iOS

- Ошибки при работе с сетью — штатная ситуация
- Сеть может быть медленная
- Сети может вообще не быть
- Загрузка данных может стоить пользователю денег :)

### Как жить
<!-- .element: class="fragment" data-fragment-index="1" -->

- Проверяем доступность сервера
<!-- .element: class="fragment" data-fragment-index="1" -->
- Обрабатываем возможные ошибки сети
<!-- .element: class="fragment" data-fragment-index="1" -->
- Обрабатываем возможные ошибки в формате данных
<!-- .element: class="fragment" data-fragment-index="1" -->
- Ограничиваем количество одновременных запросов
<!-- .element: class="fragment" data-fragment-index="1" -->
- Один большой запрос быстрее, чем много маленьких
<!-- .element: class="fragment" data-fragment-index="1" -->
- Никогда не работаем с сетью в главном потоке
<!-- .element: class="fragment" data-fragment-index="1" -->
- Уважаем пользователя: экономим трафик, кэшируем что можно, показываем спиннер
<!-- .element: class="fragment" data-fragment-index="1" -->
				</script></section>									
				
				
				
				<section data-markdown><script type="text/template">
## Загрузка в NSData

- Самый простой способ загрузить данные из сети (в одну строку)
- Сам по себе способ *синхронный* (блокирует текущий поток)
- Практически не применим в реальной работе:
  - Слабая обработка ошибок
  - Только HTTP GET
  - Нет управления заголовками
  - Нет докачки
  - ...
				</script></section>



				<section>
					<h2>Загрузка в NSData</h2>

					Выполним синхронную загрузку данных:

					<pre><code data-noescape>
NSURL *url = [NSURL URLWithString:@"http://server.org/some/path"];
<mark class="highlight-block">
NSData *data = [NSData dataWithContentsOfURL:url];
</mark>
// Данные загружены, можно использовать.
// ...
					</code></pre>
				</section>

				<section data-markdown><script type="text/template">
## NSURLConnectionDelegate

- Проверить код ответа. Подготовиться к получению данных (выделить/очистить буфер для данных).

        - (void)connection:(NSURLConnection *)connection
            didReceiveResponse:(NSURLResponse *)response

- Сохранить полученные данные. Обновить прогресс-бар, если он есть.

        - (void)connection:(NSURLConnection *)connection
            didReceiveData:(NSData *)data
        
- Обработать завершение запроса (данные уже получены/отправлены).

        - (void)connectionDidFinishLoading:(NSURLConnection *)connection

- Обработка ошибок, ...
				</script></section>