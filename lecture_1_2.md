# 1.2 Основы паттернов ООП

### Noveo University — iOS

#### Александр Горбунов


----

## Сегодня

* MVC
* Delegate
* Observer
* Singleton

... красивые названия для обыденных вещей
<!-- .element: class="fragment" -->


----

## Model-View-Controller

### View
* то, что видит пользователь
* переиспользуется для  разных данных


----

## Model-View-Controller

### View

```
UIView
UILabel
UITextField
UIButton
UISwitch
UIToolbar
UITableView
UIImageView
...
```


----

## Model-View-Controller

### Controller
* соединяет объекты-модели с объектами-видами
* бизнес-логика
* управляет жизненным циклом приложения
* обрабатывает действия пользователя


----

## Model-View-Controller

### Controller

```
UIApplicationDelegate
UIViewController
UINavigationController
UITabBarController
...
```


----

## Model-View-Controller

### Model
* хранение данных
* бизнес-логика
* может иметь разные представления
* может "общаться" с другой моделью


----

## Model-View-Controller

### Model

```
кастомные классы с данными
...
NSArray
NSDictionary
NSString
...
NSURLConnection
CLLocationManager
...
```

`NSURLConnection`, `CLLocationManager` — для клиентского кода это модель. Сами для себя эти классы — система, имеющая свою модель и контроллер на более низком уровне абстракции.


----

## Model-View-Controller

Model — Controller — View


----

## Model-View-Controller

![](lecture_1_2_img/TV_1.png)


----

## Model-View-Controller

![](lecture_1_2_img/TV_2.png)


----

## Delegate

![](lecture_1_2_img/TV_3.png)

