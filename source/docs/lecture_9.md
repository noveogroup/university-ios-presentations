# 9. KVC, KVO

### Noveo University — iOS



----

## Сегодня

* `Key-Value Coding`
* `Key-Value Observing`
* `NSPredicate`


----

## Key-Value Coding

**KVC** — механизм, позволяющий обращаться к значению (`Value`) свойства объекта, используя строковые идентификаторы — ключи (`Key`).

`KVC` основывается на методах протокола `NSKeyValueCoding`.

`KVC` предоставляет:
* Доступ к свойствам объекта.
* Доступ к свойствам в коллекциях. Вызов операторов коллекций на объектах в коллекциях.
* Доступ к скалярным свойствам.
* Доступ к свойствам по `KeyPath`.


----

## Key-Value Coding

*Использование строковых идентификаторов* позволят решить к какому свойству объекта обратиться *во время выполнения* (в runtime).

```ObjectiveC
NSString *valueB = [myObject valueForKey:@"someString"];
NSString *valueC = [myObject valueForKeyPath:@"parentObject.someString"];
```


----

## Key-Value Coding

Есть задача: нужно создать массив объектов `Person`: 

```ObjectiveC
@interface Person : NSObject
@property (nonatomic, copy) NSString *name;
@property (nonatomic, strong) NSNumber *age;
@end
```

из полученного от сервера JSON:

```
[
    {
        "name": "Alice",
        "age": 22,
        ...
    },
    {
        "name": "Bob",
        "age": 24,
        ...
    }
]
```


----

## Key-Value Coding

Решение 1: вручную работаем с каждым свойством.

```ObjectiveC
NSArray<NSDictionary *> *personsDescriptions = ...; // сериализуем JSON
NSMutableArray<Person *> *persons = [NSMutableArray array];
	
for (NSDictionary *personDescription in personsDescriptions) {
	 Person *person = [[Person alloc] init];

    person.name = personDescription[@"name"];
    person.age = personDescription[@"age"];
    
    [persons addObject:person];
}
```


----

## Key-Value Coding

Решение 2: автоматический проход по всем свойствам.

```ObjectiveC
NSArray<NSDictionary *> *personsDescriptions = ...; // сериализуем JSON
NSMutableArray<Person *> *persons = [NSMutableArray array];

for (NSDictionary *personDescription in personsDescriptions) {
	Person *person = [[Person alloc] init];

	for (NSString *key in personDescription.allKeys) {
		[person setValue:personDescription[key] forKey:key];
	}
	
	[persons addObject:person];
}
```


----

## Key-Value Coding

```
@property NSString *name;
@property NSNumber *age;
```
```
{
	"name": ...,
	"age": ...,
}
```

НО! **мы сами отвечаем за совпадение ключей**.


----

## Key-Value Coding

`KVC` позволяет включать в `KeyPath` не только простые свойства, но и коллекции объектов.

В примере на выходе мы получим коллекцию, аггрегирующую значения свойства у всех элементов коллекции.

```ObjectiveC
@interface Person : NSObject
@property (nonatomic, copy) NSString *name;
@property (nonatomic, strong) NSNumber *age;
@end
```

```ObjectiveC
@interface Department : NSObject
@property (nonatomic, copy) NSArray<Person *> *staff;
@end
```

```ObjectiveC
NSArray *allNames = [department valueForKeyPath:@"staff.name"];
// allNames: @[@"Alice", @"Bob"]
```


----

## Key-Value Coding

`KVC` предоставляет несколько операторов для обработки значений элементов коллекции: `@avg`, `@max`, `@min`, `@sum`, `@count` и др.

```ObjectiveC
@interface Person : NSObject
@property (nonatomic, copy) NSString *name;
@property (nonatomic, strong) NSNumber *age;
@end
```

```ObjectiveC
@interface Department : NSObject
@property (nonatomic, copy) NSArray<Person *> *staff;
@end
```

```ObjectiveC
NSNumber *avgAge = [department valueForKeyPath:@"staff.@avg.age"];
// avgAge: @23
```


----

## NSPredicate

Класс `NSPredicate` используется для определения логических условий, используемых для выборки или для фильтрации.
* `NSPredicate` позволяет делать достаточно хитрые запросы, в том числе при доступе к значениям через KVC.
* Синтаксис выражений похож на SQL запросы и может использовать регулярные выражения.

```ObjectiveC
@interface Person : NSObject
@property (nonatomic, copy) NSString *name;
@property (nonatomic, strong) NSNumber *age;
@end
```

```ObjectiveC
@interface Department : NSObject
@property (nonatomic, copy) NSArray <Person *> *staff;
@end
```

```ObjectiveC
NSPredicate *predicate = [NSPredicate predicateWithFormat:@"name CONTAINS 'Bob'"];
NSArray <Person *> *bobs = [department.staff filteredArrayUsingPredicate:predicate];

predicate = [NSPredicate predicateWithFormat:@"age >= 19 AND age < 26"];
NSArray<Person *> *somePersons = [department.staff filteredArrayUsingPredicate:predicate];
```


----

## Key-Value Coding

Значения при использовании `KVC` являются объектами и имеют тип `id`, поэтому:
* При обращении к скаляру (`BOOL`, `NSInteger`, `double`, ...) через KVC, он автоматически оборачивается в `NSNumber`.
* При обращении к структуре (`struct`) через `KVC`, она автоматически оборачивается в `NSValue`.
* При присвоении значения `nil` скаляру через `KVC`, вызывается метод `setNilValueForKey:`, в котором нужно определить желаемое поведение. По умолчанию этот метод вызовет исключение `NSInvalidArgumentException`.


----

## Key-Value Coding

По умолчанию обращение по несуществующему ключу вызывает исключение, поэтому нужно реализовать одну из политик:
* Гарантированно не обращаться к несуществующим ключам.
* Переопределить методы, обрабатывающие обращение к несуществующим ключам `valueForUndefinedKey:` и `setValue:forUndefinedKey:`.


----

## Key-Value Coding

Для поддержки работы KVC нужно правильно именовать методы-акцессоры:
* Имя геттера должно совпадать с именем свойства.
* Имя геттера `BOOL`-свойства должно иметь префикс `is`.
* Имя сеттера должно иметь префикс `set`.
* Имя переменной экземпляра должно совпадать с именем свойства и может иметь префикс `_`.

```ObjectiveC
@property (nonatomic, copy) NSString *name;
```
```ObjectiveC
- (NSString *)name {...}
- (void)setName:(NSString *)name {...}
```


----

## Key-Value Coding

Справочная литература:
* [Key-value coding](https://developer.apple.com/library/content/documentation/General/Conceptual/DevPedia-CocoaCore/KeyValueCoding.html)
* [About Key-Value Coding](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/KeyValueCoding/)
* [KVC Collection Operators](http://nshipster.com/kvc-collection-operators/)
* [NSPredicate](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/Predicates/AdditionalChapters/Introduction.html#//apple_ref/doc/uid/TP40001798-SW1)
* [NSPredicate](https://developer.apple.com/reference/foundation/nspredicate?language=objc)
* [NSPredicate](http://nshipster.com/nspredicate/)



----

## Key-Value Observing

**KVO** — механизм, автоматизирующий нотификацию об изменениях свойств объекта. `KVO` является стандартной (встроенной) реализацией паттерна `Observer`.


----

## Key-Value Observing

Чтобы реализовать получение нотификаций, необходимо:

* Подписаться на нотификации, указав получателя, объект и `KeyPath` для отслеживания, контекст, дополнительные опции (например нотификация до или после изменения значения).
* Обрабатывать полученные нотификации, проверив что они действительно должны быть обработаны. (Родительский класс мог так же подписаться на нотификации и их нужно передать в `super`).
* По необходимости или в конце жизненного цикла отписаться от всех ранее созданных подписок.


----

## Key-Value Observing

KVO — мощный механизм, который не терпит ошибок...

![](./lecture_9_img/flamethrower.gif)


----

## Key-Value Observing

* Создаём контекст. Он поможет определить, принадлежат ли объекту полученные нотификации.
  ```ObjectiveC
  static void *const myContext = (void *)&myContext;
  ```

* Подписываемся на изменения значений (например в `init`).
  ```ObjectiveC
  [self.myPerson addObserver:self forKeyPath:@"name"
      options:NSKeyValueObservingOptionNew context:myContext];
  ```

* Отписываемся от нотификаций (например в dealloc).
  ```ObjectiveC
  [self.myPerson removeObserver:self forKeyPath:@"name" context:myContext];
  ```


----

## Key-Value Observing

* Получаем и обрабатываем нотификации

```ObjectiveC
- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object
    change:(NSDictionary *)change context:(void *)context
{
	if (context != myContext) {
		[super observeValueForKeyPath:keyPath ofObject:object
			change:change context:context];
		return;
	}

	Person *person = (Person *)object;
	NSLog(@"New value is %@.", person.name);
}
```


----

## Key-Value Observing

`KVO` поддерживает вычисляемые свойства (не имеющие под собой ivar, значение вычисляется в геттере).

```ObjectiveC
@property (nonatomic, copy) NSString *firstName;
@property (nonatomic, copy) NSString *lastName;
@property (nonatomic, readonly) NSString *fullName;
```
```ObjectiveC
- (NSString *)fullName
{
	return [NSString stringWithFormat:@"%@ %@", self.firstName, self.lastName];
}
```


----

## Key-Value Observing

`KVO` поддерживает вычисляемые свойства.

Выразить зависимости можно с помощью методов:
```ObjectiveC
+ (NSSet *)keyPathsForValuesAffectingValueForKey:(NSString *)key
+ (NSSet *)keyPathsForValuesAffecting<Key>
```

```ObjectiveC
+ (NSSet *)keyPathsForValuesAffectingValueForKey:(NSString *)key {
	NSSet *keyPaths = [super keyPathsForValuesAffectingValueForKey:key];
	
	if ([key isEqualToString:@"fullName"]) {
		NSArray *affectingKeys = @[@"lastName", @"firstName"];
		keyPaths = [keyPaths setByAddingObjectsFromArray:affectingKeys];
	}
	
	return keyPaths;
}
```
или
```ObjectiveC
+ (NSSet *)keyPathsForValuesAffectingFullName {
    return [NSSet setWithObjects:@"lastName", @"firstName", nil];
}

```


----

## Key-Value Observing

`KVO` поддерживает отслеживание изменений содержимого коллекций. Однако для обеспечения работоспособности этого механизма, изменения должны происходить не напрямую в коллекции, а через прокси-объект:

```ObjectiveC
@property (nonatomic) NSArray<Person *> *staff;
```

```ObjectiveC
NSMutableArray<Person *> *mutableStaff = [self mutableArrayValueForKey:@"staff"];
[mutableStaff addObject:newEmployee];
```


----

## Key-Value Observing

Основыные правила:
* Все нотификации приходят в один метод-обработчик.
* При переименовании свойства мы ответственны за обновление всех `KeyPath`-строк.
* Каждый объект должен обрабатывать только "свои" нотификации. Нельзя отдавать в `super` свою нотификацию, не стоит обрабатывать нотификации, предназначенные для `super`.
* Если кто-то использует свойство для `KVO`, к нему нельзя обращаться через `ivar`, или нужно вручную нотифицировать об изменении значения (`willChangeValueForKey:` / `didChangeValueForKey:`).


----

## Key-Value Observing

Основыные правила:
* Нельзя не отписываться от нотификаций.
* Нельзя отписываться дважды от одной и той же нотификации.
* Нельзя проверить, подписан ли объект на нотификацию.


----

## Key-Value Observing

Для избавления от страданий создано много обёрток над API KVO.

* [KVOBlocks](https://github.com/sleroux/KVO-Blocks)
* [KVOController](https://github.com/facebook/KVOController)
* [ReactiveCocoa](https://github.com/ReactiveCocoa/ReactiveCocoa)




----

## Key-Value Observing

Справочная литература:
* [Key-value observing](https://developer.apple.com/library/content/documentation/General/Conceptual/DevPedia-CocoaCore/KVO.html)
* [Key-Value Observing Programming Guid](https://developer.apple.com/library/content/documentation/Cocoa/Conceptual/KeyValueObserving/KeyValueObserving.html#//apple_ref/doc/uid/10000177-BCICJDHA)
* [Understanding Key-Value Observing and Coding](http://www.appcoda.com/understanding-key-value-observing-coding/)
* [Key-Value Coding and Observing](https://www.objc.io/issues/7-foundation/key-value-coding-and-observing/)


