# 3 Управление памятью

### Noveo University — iOS

#### Дмитрий Горев


----

## Сегодня

* Основы управления памятью
* Manual Retain-Release
* Automatic Reference Counting


----

## Типы памяти

* __Статическая память__ содержит глобальные и статические скалярные переменные и ссылки на объекты
* __Локальная (стековая) память__ выделяется при входе в подпрограмму (метод, функцию) и освобождается при выходе из нее
* __Динамическая память__ выделяется в рантайме и управляется кодом


----

## Управление динамической памятью

* Динамическое выделение памяти
* Использование выделенной памяти
* Высвобождение выделенной памяти


----

## Виды управления памятью

* Ручное управление
  * new, calloc, malloc, delete, free
  * Smart pointers (Boost / STL)
  * Manual Retain-Release (MRR)
* Автоматическое управление
  * Garbage collection (GC)
  * Automatic Reference Counting (ARC)


----
<!--
## Проблемы ручного управления памятью

* Освобождение (перезапись) данных, которые все еще используются
* Исполнение программы без освобождения памяти, занятой более ненужными данными


---->

## Эффективное управление памятью

Использование номинально необходимого объема выделяемой памяти, достигается за счет:
* Выделения памяти по необходимости
* Совместного использования данных
* Своевременного удаления ненужных объектов (данных)


----

# Manual Retain-Release


----

## Основные положения

* Выделение памяти под объект (и его переменные) происходит в методе класса `alloc`
* Высвобождение памяти происходит в методе объекта `dealloc`
* Каждый объект имеет свойство-счетчик ссылок `retainCount`
* Объект умирает (вызывается метод `dealloc`) когда счетчик ссылок достигает нуля


----

## Управление счетчиком ссылок

* Методы `alloc`, `new`, `copy`, `mutableCopy` возвращают объекты с счетчиком ссылок равным единице*
* Метод `retain` увеличивает счетчик на единицу
* Метод `release` уменьшает счетчик на единицу
* Метод `autorelease` выполняет отложенное уменьшение счетчика на единицу

\*На самом деле не всегда, но мы должны так считать


----

## Пример

```ObjectiveC
NSMutableArray *array = [[NSMutableArray alloc] init];
NSLog(@"%ld", array.retainCount); //1
[array retain];
NSLog(@"%ld", array.retainCount); //2
[array retain];
NSLog(@"%ld", array.retainCount); //3
[array release];
NSLog(@"%ld", array.retainCount); //2
[array autorelease]
NSLog(@"%ld", array.retainCount); //2

NSMutableArray *arrayCopy = [array mutableCopy];
NSLog(@"%ld", arrayCopy.retainCount); //1
[arrayCopy release];
[arrayCopy release]; //Exception
```


----

## Управление памятью в пределах подпрограммы

* Создаем объекты когда они нужны
* Удаляем когда они больше не нужны
* Возвращаем "наверх" autorelease-нутые объекты


----

## Пример

```ObjectiveC
- (NSString *)getTimeOfDate:(NSDate *)date
{
    NSDateFormatter *dateFormatter = [[NSDateFormatter alloc] init];
    dateFormatter.date = @"hh:mm";
    NSString *dateString = [dateFormat stringFromDate:date];
    [dateFormat release];

    return dateString;
}
```
Упрощенный вариант
```ObjectiveC
- (NSString *)getTimeOfDate:(NSDate *)date
{
    NSDateFormatter *dateFormatter = [[[NSDateFormatter alloc] init] autorelease];
    dateFormatter.date = @"hh:mm";
    return [dateFormat stringFromDate:date];
}
```


----

## Пример

```ObjectiveC
- (NSString *)appendNewLineToString:(NSString *)string
{
    NSString *result = [[NSString alloc] initWithFormat:@"%@\n", string];
    return [result autorelease];
}
```
Упрощенный вариант
```ObjectiveC
- (NSString *)appendNewLineToString:(NSString *)string
{
    return [[[NSString alloc] initWithFormat:@"%@\n", string] autorelease];
}
```
Еще проще
```ObjectiveC
- (NSString *)appendNewLineToString:(NSString *)string
{
    return [NSString stringWithFormat:@"%@\n", string];
}
```


----

## Управление памятью в пределах объекта

К управленю памятью объекта следует подходить с позиции "владения" и "объектных графов". Для владения объектом нужно:
* Создать объект либо поработить объект, переданный извне, методом retain
* Сохранить ссылку на объект в переменной объекта-владыки
* Освободить объект когда он больше не нужен методом release или autorelease
* Освобождать все объекты-рабы в методе dealloc
* Не хранить ссылки на освобожденные объекты (занулять переменные-указатели)


----

## Пример

```ObjectiveC
@interface Person : NSObject {
    NSString *_firstName;
    NSString *_lastName;
    NSString *_fullName;
}
@end

@implementation Person

- (Person *)initWithFirstName:(NSString *)firstName lastName:(NSString *)lastName
{
    self = [super init];
    _firstName = [firstName retain];
    _lastName = [lastName retain];
    _fullName = [[NSString stringWithFormat:@"%@ %@", firstName, lastName] retain];
    return self;
}

- (NSString *)getFullName
{
    return _fullName;
}

@end
```


----

## Пример

```ObjectiveC
{
    Pupil *aPupil = [[Pupil alloc] init];
    // ...
    NSString *name = aPupil.name;
    // ...
    [aPupil release];
    aPupil = nil;
}
```


----

## Основные правила управления памятью

Вы не владеете объектами, которые вам вернули по ссылке


----

## Основные правила управления памятью

Ни при каких условиях вы не должны отказываться от прав на владение тем или иным объектом, если вы им не владеете.


----

## Пример

```ObjectiveC
{
    NSError *error = nil;
    NSString *string =
        [[NSString alloc]
            initWithContentsOfFile:fileName
            encoding:NSUTF8StringEncoding
            error:&error];
    if (string == nil) {
        // Handle the error ...
    }
    // ...
    [string release];
    string = nil;
}
```


----

## Высвобождение памяти

Метод dealloc всегда вызывается автоматически, не пытайтесь вызывать его самостоятельно.


----

## Роль метода dealloc

* Высвобождение занятой объектом памяти,
* Освобождение занятых ресурсов,
* Отказ от прав на владение любыми внутренними объектами.


----

## Пример

```ObjectiveC
@interface Pupil : NSObject
@property (retain) NSString *name;
@end

@implementation Pupil
//...
- (void)dealloc
{
    [name release];
    name = nil;
    [super dealloc];
}
@end
```


----

## Переопределение метода dealloc

* Вы обязаны вызвать [super dealloc]
* Ни при каких обстоятельствах не помещайте код, управляющий системными ресурсами, в переопределенную реализацию метода



----

## Классификаторы времени жизни

К свойствам объектов применимы следующие классификаторы
* retain
* copy
* readonly
* readwrite (по умолчанию для скалярных типов)
* assign (по умолчанию для объектов)


----

## "Слабое" связывание объектов

* Решает проблему циклических ссылок
* Не оказывает влияния на счетчик ссылок
* Классификатор assign


----

## Пример

```ObjectiveC
@interface UITableView : UIScrollView <NSCoding>
//...
@property (nonatomic, assign)
    id<UITableViewDataSource> dataSource;
@property (nonatomic, assign)
    id<UITableViewDelegate> delegate;
//...
```


----

# Autorelease Pools


----

## Autorelease pools

* Механизм, предоставляющий возможность отказаться от прав владения объектом, избегая немедленного высвобождения памяти
* Все объекты, получившие сообщение autorelease, остаются в памяти до тех пор, пока жив pool, в котором объект получил это сообщение


----

## Autorelease pools

Обычно вам не нужно создавать подобного рода объекты, за исключением нескольких особых случаев


----

## Особые случаи

Вы работаете над приложением, которое не базируется на UI framework


----

## Особые случаи

Вы работаете над неким циклом, который порождает множество временных объектов


----

## Особые случаи

Вы работаете над многопоточным приложением. Каждый новый поток должен иметь собственный autorelease pool к моменту запуска.


----

## Принцип действия

При уничтожении autorelease pool рассылает сообщение release всем связанным с ним объектам, которые до момента уничтожения получили сообщение autorelease.

Число рассылаемых сообщений release равно числу разосланных autorelease.


----

## Пример

```ObjectiveC
{
    // ...
    NSAutoreleasePool *const pool =
        [[NSAutoreleasePool alloc] init];

    // Code that creates autoreleased objects.

    [pool release];
    // ...
}
```


----

# Automatic Reference Counting


----

## Переход на ARC

* Концептуально ARC идентичен MRR
* В отличии от MRR, подсчет ссылок осуществляется автоматически
* Все необходимые для управления памятью вызовы расставляются за вас на этапе компиляции


----

## Преимущества ARC

* Лишен недостатков, присущих ручным способам управления памятью
* Уменьшает объем кода
* Уменьшает время разработки
* Нарушение установленных правил управления памятью приводит к ошибке компиляции


----

## Когда использовать ARC?

“You are strongly encouraged to use ARC for new projects.”

Copyright © 2012 Apple Inc. All Rights Reserved.


----

## Ограничения накладываемые ARC

Запрещено вызывать:
* retain
* release (autorelease)
* [super dealloc]


----

## Классификаторы времени жизни

Множество классификаторов, применимых к свойствам объектов, дополнено:
* strong (по умолчанию для объектов)
* weak
* unsafe_unretained


----

## Классификаторы времени жизни

К переменным применимы следующие классификаторы:
* __strong (по умолчанию для объектов)
* __weak
* __unsafe_unretained
* __autoreleasing


----

## Классификаторы времени жизни

Оформляйте классификаторы правильно!

ClassName *qualifier variable;


----

## Пример

```ObjectiveC
// ...

MyClass *__weak weakReference = ...;

MyClass *__unsafe_unretained unsafeReference = ...;

// ...
```


----

## Пример

```ObjectiveC
{
    // ...
    NSString *__weak string =
        [[NSString alloc] initWithFormat:
            @"First Name: %@", [self firstName]];
    NSLog(@"string: %@", string);
    // ...
}
```


----

## Пример

```ObjectiveC
{
    // ...
    NSError *error;
    BOOL OK = [object doSomethingWithError:&error];
    if (!OK) {
        // ...
    }
}
```


----

## Включение/выключение ARC

При помощи флагов компилятора
* -fobjc-arc,
* -fno-objc-arc (для отдельных файлов).


----

# Autorelease Pool Blocks


----

## Autorelease Pool Blocks

* Концептуально блоки ничем не отличаются от объектов,
* Отличие состоит только в синтаксической записи.


----

## Пример

```ObjectiveC
{
    // ...
    @autoreleasepool {
        // Code that creates autoreleased objects.
    }
    // ...
}

```


----

## Диагностика управления памятью

* Clang Static Analyzer
* Developer Tools - Instruments

