# 3 Управление памятью

### Noveo University — iOS

#### Дмитрий Горев


----

## Сегодня

* Основы управления памятью
* Manual Retain-Releases
* Automatic Reference Counting


----

## Управление памятью

* Динамическое выделение памяти
* Использование выделенной памяти
* Высвобождение выделенной памяти


----

## Проблемы ручного управления памятью

* Освобождение (перезапись) данных, которые все еще используются
* Исполнение программы без освобождения памяти, занятой более ненужными данными


----

## Виды управления памятью

* Ручное управление
  * new, calloc, malloc, delete, free
  * Smart pointers (Boost / STL*)
  * Manual Retain-Release (MRR)
* Автоматическое управление
  * Garbage collection (GC)
  * Automatic Reference Counting (ARC)

* "Умные" указатели стали частью STL только со вступление в силу стандарта C++11


----

## Эффективное управление памятью

Использование номинально необходимого объема выделяемой памяти, достигается за счет:
* Выделения памяти по необходимости
* Совместного использования данных
* Своевременного удаления ненужных объектов (данных)


----

## Диагностика управления памятью

* Clang Static Analyzer
* Developer Tools - Instruments


----

# Manual Retain-Release


----

## Основные правила управления памятью

К управленю памятью следует подходить с позиции "владения" и "объектных графов"
* Объектный граф - группа объектов, которые соединены в сеть посредством установления тех или иных отношений между ними


----

## Основные правила управления памятью

Вы владеете любым объектом, который создаете

Для создания объекта используются методы, начинающиеся с alloc, new, copy, mutableCopy


----

## Основные правила управления памятью

Вы должны отказаться от права владения объектом тогда, когда он больше не нужен

Для отказа достаточно послать объекту одно из сообщений release или autorelease


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

## Пример

```ObjectiveC
- (NSString *)fullName
{
    NSString *fullName =
        [[[NSString alloc] initWithFormat:@”%@ %@”,
            self.surname, self.name] autorelease];

    return fullName;
}
```


----

## Пример

```ObjectiveC
- (NSString *)fullName
{
    NSString *fullName =
        [NSString stringWithFormat:@”%@ %@”,
            self.surname, self.name];

    return fullName;
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

* Осуществляется автоматически как только счетчик ссылок достигает значения 0
* Всегда сопряжено с вызовом метода dealloc (определен в классе NSObject) у того объекта, который будет удален из памяти


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
