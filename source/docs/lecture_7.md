# 7. Асинхронность

### Noveo University — iOS



----

## Сегодня

* Потоки, `NSThread`
* Очереди, `Grand Central Dispatch`, `NSOperation/NSOperationQueue`



----

## Асинхронность в iOS

* Все операции с UI нужно выполнять в главном потоке.
* Все долгие операции нужно выполнять не в главном потоке.
* Нельзя обращаться к изменяемому объекту из разных потоков.
* Результат работы не должен зависеть от порядка выполнения асинхронных операций.
* Распараллеливание независимых операций может ускорить работу программы.


----

## Асинхронность в iOS

### Поток

* "Бесконечные" и пошаговые вычисления.
* Организация RunLoop.
* Явное управление порядком исполнения.


----

## `NSThread`

* Используется для длительных или бесконечных задач.
* Явное создание потока (нужно использовать с умом).
* Создание потока — дорогая операция.


----

## Создание `NSThread`

* Исполняем уже имеющийся метод:

  ```ObjectiveC
  NSThread *thread = [[NSThread alloc] initWithTarget:self
  	selector:@selector(calculate) object:nil];

  [thread start];
  ```

* Создаём подкласс `NSThread`, переопределяем метод `main`, у экземпляра класса вызываем `start`.


----


## Асинхронность в iOS

### Очередь

* Логически обособленные задачи.
* Балансировка загрузки ядер ЦП.
* Организация цепочки задач на высоком уровне.



----


## GCD

*Grand Central Dispatch*

* Лучшая производительность.
* Относительно низкоуровневое API на языке C.
* Используется для быстрого перехода между главным и фоновым потоками.
* Для простых задач — короткая запись.
* Поддержка очередей, групп, таймеров, ...


----

## GCD - Synchronous vs. Asynchronous


- Synchronous - `dispatch_sync`
- Asynchronous - `dispatch_async`



----


## GCD - типы очередей

- С последовательным выполнением задач (Serial) 
- С параллельным выполнением задач (Concurrent)



----

## GCD

Пример выполнения асинхронной операции:

```ObjectiveC
dispatch_queue_t queue =
	dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);
	
dispatch_async(queue, ^{
	// Блок выполняется асинхронно.
    ...
});

// Программа продолжает выполняться, не дожидаясь выполнения блока.
...
```


----

## GCD

Пример перехода в главную очередь после выполнения асинхронной операции:

```ObjectiveC
dispatch_queue_t queue =
	dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0);
	
dispatch_async(queue, ^{
		// Блок выполняется асинхронно.
    	...
    	
    	dispatch_async(dispatch_get_main_queue(), ^{
				// Блок выполняется на главной очереди.
				// Можно обновить UI, используя асинхронно полученные данные.
				...
	    	});
	});
	
// Программа продолжает выполняться, не дожидаясь выполнения блоков.
...
```


----

## GCD

```ObjectiveC
dispatch_queue_t queue1 = dispatch_queue_create("MyQueue1", NULL); // Serial queue
dispatch_queue_t queue2 = dispatch_queue_create("MyQueue2", NULL); // Serial queue
	
void (^myBlock1)(void) = ^ {/*...*/};
void (^myBlock2)(void) = ^ {/*...*/};
void (^myBlock3)(void) = ^ {/*...*/};
	
dispatch_async(queue1, myBlock1);
dispatch_async(queue2, myBlock2);
dispatch_async(queue2, myBlock3);
```

```
QUEUE 1: |—————————block 1—————————|

QUEUE 2: |————block 2————| |——block 3——|

Время ————————————————————————————————————————>
```


----

## GCD - группы

```ObjectiveC
dispatch_group_t group = dispatch_group_create(); // Создание новой группы
	
dispatch_group_enter(group); // Метка о входе в группу,
// увеличивает кол-во незавершенных задач
[SomeClassThatLoadsOffTheInternet getMyImages:^{ // do something with these.
	dispatch_group_leave(group); // Метка о завершении работы и выходе из группы
});

dispatch_group_enter(group);
[SomeClassThatLoadsOffTheInternet getMyText:^{ // do something with these.
	dispatch_group_leave(group);
});

// Можно синхронно дождаться завершения всех задач
dispatch_group_wait(group, DISPATCH_TIME_FOREVER); // or
// Можно продолжить выполнение программы
// По завершению задач, вызвать блок
// dispatch_group_notify(group, queue, ^{
//    ...
// });

```


----

## `NSOperation / NSOperationQueue`

* Используется для логически обособленных задач.
* Поддержка отмены операций.
* Поддержка графа зависимостей между операциями.
* Поддержка приоритезации операций.
* Повторное использование операций.
* Контроль над всей очередью (пауза, возобновление, отмена всех запросов).
* Эффективное использование системных ресурсов (потоки создаются автоматически, если необходимо).



----

## `NSOperation`

Объявление и запуск двух блоковых операций:

```ObjectiveC
NSBlockOperation *operation1 = [NSBlockOperation blockOperationWithBlock:^{
		...
	}];
	
NSBlockOperation *operation2 = [NSBlockOperation blockOperationWithBlock:^{
		...
	}];
	
NSOperationQueue *queue = [[NSOperationQueue alloc] init];
[queue addOperation:operation1];
[queue addOperation:operation2];
```


----

## `NSOperation`

Задание приорететов и зависимостей операций:

```ObjectiveC
NSOperation *operation1, *operation2, *operation3;
NSOperationQueue *queue;

...

operation1.queuePriority = NSOperationQueuePriorityLow;
operation2.queuePriority = NSOperationQueuePriorityHigh;
	
[operation3 addDependency:operation1];
[operation3 addDependency:operation2];
	
[queue addOperation:operation1];
[queue addOperation:operation2];
[queue addOperation:operation3];
```


----

## `NSOperation`

Объявление операции из метода и кастомного объекта-операции:

```ObjectiveC
NSOperation *operation1, *operation2;
NSOperationQueue *queue;

...
	
operation1 = [[NSInvocationOperation alloc] initWithTarget:self
	selector:@selector(printCount) object:nil];
	
operation2 = [[MyCustomOperation alloc] init];
	
[queue addOperation:operation1];
[queue addOperation:operation2];
```


----




## Потокобезопасность

```ObjectiveC
+ (Singleton *)sharedInstance
{
	static Singleton *_sharedInstance = nil;
	if (!_sharedInstance) {
		_sharedInstance = [[Singleton alloc] init];
	}
	return _sharedInstance;
}
```

Что произойдёт, если вызвать `sharedInstance` из двух разных потоков "одновременно", когда объект ещё не создан?


----

## Потокобезопасность

Используем dispatch-once:

```ObjectiveC
+ (Singleton *)sharedInstance
{
	static Singleton *_sharedInstance = nil;

	static dispatch_once_t token;
	dispatch_once(&token, ^{
		_sharedInstance = [[Singleton alloc] init];
	});

	return _sharedInstance;
}
```


----

## Потокобезопасность

```ObjectiveC 
- (void)didReceiveSomeStringFromNetwork:(NSString *)someString
{
	self.someString = someString;
	[self showCurrentData];
}

- (void)showCurrentData
{
	self.someLabel.text = self.someString;
}
```

Что произойдёт когда мы получим новые данные по сети (в фоновом потоке)?


----

## Потокобезопасность

При работе с UI нужно перейти в главный поток.

```ObjectiveC 
- (void)didReceiveSomeStringFromNetwork:(NSString *)someString
{
	self.someString = someString;
	
	dispatch_async(dispatch_get_main_queue(), ^{
		[self showCurrentData];
	});
}

- (void)showCurrentData
{
	self.someLabel.text = self.someString;
}
```



----

## Потокобезопасность

При работе со свойствами из разных потоков имеет смысл объявить их как `atomic`.

```ObjectiveC
@property (atomic) NSString *string;
```


----

## Потокобезопасность

При работе с изменяемыми объектами из разных потоков, `atomic` не спасёт, т.к. относится только к *указателю*, но не к объекту.

```ObjectiveC
@property (atomic) NSMutableArray *tasks;
```


----

## Потокобезопасность

Однако мы можем вынести обращения к такому свойству в последовательную очередь.

```ObjectiveC
@property (atomic) NSMutableArray *tasks;
@property (atomic) dispatch_queue_t tasksQueue;
```

```ObjectiveC
- (instancetype)init
{
	self = [super init];
    if (self) {
        _tasksQueue = dispatch_queue_create("com.myDomain.myApp.tasksQueue", NULL);
    }
    return self;
}

- (Task *)taskByIndex:(NSUInteger)index
{
	__block Task *localTask = nil;
	dispatch_sync(self.tasksQueue, ^{ // Синхронное чтение
		localTask = [self.tasks objectAtIndex:index];
	});
	return localTask;
}

- (void)addTask:(Task *)task
{
	dispatch_async(self.tasksQueue, ^{ // Асинхронная запись
		[self.tasks addObject:task];
	});
}
```


