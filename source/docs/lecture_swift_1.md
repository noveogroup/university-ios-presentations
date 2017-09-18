# 1. Введение в Swift. Часть 1

### Noveo University — iOS


----
## Структура программы

* отсутствуют заголовочные файлы
* нет явного разделения интерфейса и реализации, вся информация о классах, функциях и константах находится в единственном `*.swift` файле.
* любой `Objective-C` фреймворк или `C` библиотека может быть импортирована напрямую в `Swift` проект. Это включает все системные фреймворки

```swift
import Foundation
```
<!-- после такого импорта в свифт файле будут доступны все классы, протоколы, функции и константы из фреймворка Foundation -->


----
## Примитивы
<!-- Слайд для напоминания синтаксиса --->

```swift
	let x = 1 // Int
	let d = 1.0 // Double
	let f: Float = 1 // Float
	let s = "example" // String
	var result = "example" + String(x) // example 1
	result = "\(s) \(x * 2)" // example 2
	
	/* multiline example */
	let multiline = """
		This is a test example
			of the multiline string
	"""
```

<!-- Рассказать про строки, characters и кластеры. Почему string.count - это не то, что кажется -->

<!-- Описание работы с функцией вывода в лог -->

```swift
	func print(_ items: Any..., 
				separator: String = default, 
			 	terminator: String = default)
	
	let one = "1"; let two = "2"; let three = "3" // semicolon between statements
	
	print(one, two, three) // prints 1 2 3\n
	print("1", "2", "3", separator: ".", terminator: "!") // prints 1.2.3!
```


----
## Числовые типы данных

У базовых числовых типов данных определены границы допустимых значений
```swift
	let min = UInt8.min // 0
	let max = UInt8.max // 255
```
В большинстве случаев вам не понадобится указывать конкретный размер для целого числа. Для этого случая в `Swift` определëн тип `Int`, который по размеру равен разрядности операционной системы. 

<!-- Обратить внимание, что это может быть источником проблем на старых устройствах с 32-разрядным Int, в который могут не влезть данные -->


----
## Числовые типы данных
Для операций с вещественными числами определены типы 
* `Float` (32 бита, 6 цифр после запятой);
* `Double` (64 бита и как минимум 15 цифр после запятой).

Для удобства преобразований
```swift
	let million = 1_000_000
	let overMillion = 1_000_000.000_000_1
	
	let binary = 0b11001 // 25 в двоичной системе счисления
	let octal = 0o31 // 25 в восьмиричной
	let hex = 0x19 // 25 в шестнадцатеричной
	let exp1 = 1.5e3 // 1500
	let exp2 = 1.5e-3 // 0.0015
	let hExp1 = 0x11p4 // 17 * 2^4 = 272
	let hExp2 = 0x11p-4 // 17 * 2^(-4) = 1.0625
```


----
## Выход за пределы

```swift
	let notNegative: UInt8 = -1
	// Negative integer '-1' overflows when stored into unsigned type 'UInt8'
	
	let tooBig: Int8 = Int8.max + 1
	// Arithmetic operation '127 + 1' (on type 'Int8') results in an overflow
```

Решить можно двумя способами. 
* Либо определять тип результата таким образом, чтобы в него явно помещалось итоговое значение
```swift
	let variable: Int16 = Int8.max + 1
```
* Либо использовать безопасные операторы
```swift
	let variable: UInt8 = UInt8.max &+ 2 // 1
```


----
## Кортеж (Tuple)
В `Swift` встроена возможность создания анонимного типа данных простым объединением нескольких типов в одну группу. Например
```swift
	let http404Error = (404, "Not Found")
	let (justCode, _) = http404Error
	let http200Status = (statusCode: 200, description: "Ok")
	print(http200Status.statusCode)
```
Для удобства любому кортежу можно назначить имя 
```swift
	typealias Void = ()
	typealias HttpResponseStatus = (statusCode: UInt16, description: String)
```
Если ваша структура данных будет использоваться за пределами какой-то малой области логики, то используйте полноценные структуры и классы вместо кортежей.
<!-- является value-type -->


----
## Коллекции. Массив
```swift
	// Array<Element>
	let array = ["cat", "dog"]
	let emptyArray = Array<String>()
	var emptyArray2: [String] = []
	emptyArray2[0] = "some"
	emptyArray2.removeFirst()
	
	var repeating = Array(repeating: 0, count: 10) //0000000000
	repeating[3...8] = [1, 1] // 000110
	// 3...8  CountableClosedRange<Int>
	// 3..<9  CountableRange<Int>
	
	let sum = ["woman"] + ["man"] // ["woman", "man"]
```
* Определëн как обобщëнная коллекция (generic)
* Является value-type
* Объявляйте через `let` когда возможно (простота и оптимизация)


----
## Коллекции. Словарь
<!-- Рассказать о хэш-таблице и о Hashable -->
```swift
	// Dictionary<Key, Value>; Key must be Hashable
	let dictionary = ["key1": 7, "key2": 14, "key3": 21]
	let emptyDictionary = Dictionary<String, Int>() 
	var emptyDictionary2: [String: Int] = [:]
	emptyDictionary2["key"] = 0
	let old = emptyDictionary2.removeValue(forKey: "key")
```
* Определëн как обобщëнная коллекция (generic)
* Является value-type
* Элементы не упорядочены
* Объявляйте через `let` когда возможно (простота и оптимизация)


----
## Коллекции. Множество
```swift
	// Set<Element>; Key must be Hashable
	
	let emptySetOfChar = Set<Character>()
	
	var setOfInt: Set<Int> = [0, 3, 2, 99]
	setOfInt.insert(1)
	let contains = setOfInt.contains(99)
	let removed = setOfInt.remove(10)
```
* Определëн как обобщëнная коллекция (generic)
* Является value-type
* Элементы не упорядочены
* Объявляйте через `let` когда возможно (простота и оптимизация)


----
## Коллекции. Операции над множествами
Пересечения
```swift
	let odd: Set = [1, 3, 5, 7, 9]
	let even: Set = [0, 2, 4, 6, 8]
	let prime: Set = [2, 3, 5, 7]
	
	odd.union(even) // 0...9
	odd.intersection(even) // empty
	odd.subtracting(prime) // 1, 9
	odd.symmetricDifference(prime) // 1, 2, 9
```
Принадлежность
```swift
	func isSubset(of:) // проверка является ли подмножеством
	func isSuperset(of:) // проверка является ли надмножеством
	func isStrictSubset(of:) // проверка является ли подмножеством и не равно
	func isStrictSuperset(of:) // проверка является ли надмножеством и не равно
	func isDisjoint(with:) // проверка на отсутствие общих элементов
```


----
## Перечисления
```swift
	enum Some {
		case first, second 
		case third
	}
	
	let some = Some.second
	switch some {
		case .first: 
			fallthrough
		case .second: 
			print("first or second")
		default:
			break
	}
	
	enum Digit: Int {
		case zero = 0, one, two, five = 5, six, seven
	}
	print(Digit.six.rawValue) // 6
```
* Является value-type
* Поддерживает `Hashable` в указанном виде


----
## Перечисления. Ассоциированные значения
```swift
enum Barcode {
	case upc(Int, Int, Int, Int)
	case qr(String)
}
```
```swift
switch code {
	case let .upc(system, manufacturer, product, check):
		print(system, manufacturer, product, check)
	case .qr(var productCode):
		print(productCode)
}
if case let .qr(productCode) = code { /* ... */ } 

let barcodes: [Barcode] = // Some array of barcodes
for case let .qr(productCode) in barcodes {
	print(productCode)
}
```
<!-- показать возможные места для let\var -->
* Не поддерживает `Hashable`


----
## Перечисления. Вложенность
В случае если ваше перечисление содержит некоторые случаи, которые содержат в качестве ассоциированного значения объект того же перечисления, то необходимо использовать `indirect`

```swift
indirect enum ArithmeticExpression {
	case number(Int)
	case add(ArithmeticExpression, ArithmeticExpression)
}

func calculate(exp: ArithmeticExpression) -> Int {
	switch exp {
		case let .number(value):
			return value
		case let .add(first, second):
			return calculate(exp: first) + calculate(exp: second)
	}
}
```


----
## Перечисления. Ассоциированные значения
Чтобы сделать работу с перечислениями ещë более новороченной в `Swift` реализован механизм Pattern Matching.
```swift
	enum NumberExpression {
		case sum(Int, Int)
		case subtract(Int, Int)
	}
	
	func calculate(numberExpression: NumberExpression) -> Int {
		switch numberExpression {
			case let .sum(first, second) where first == second:
				return 2 * first
			case let .sum(first, second):
				return first + second
			case let .subtract(first, second):
				return first - second
		}
	}
```
```swift
	for case let .qr(productCode) in barcodes where productCode.contains("QWE") {
		print(productCode)
	}
```


----
## Optional
В `Swift` реализована обработка ситуацией отсутствия значения на уровне компиляции. Для этого определëн тип
```swift
	enum Optional<Wrapped> {
		case none
		case some(Wrapped)
	}

	var integer: Int? // default value is none
	var another: Optional<Int> = 5
	
	// Оператор ! разворачивает содержимое, но это небезопасно - runtime error
	print(another!) 
	
	if let unwrapped = integer {
		print(unwrapped) // unwrapped имеет тип Int
	}
	
	integer?.hashValue // optional chaining
	var someVariable: [Int!] //  compile error. Почему?
```
<!-- fatal error в случае nil!. Также обратить внимание, что нельзя с пробелом написать `another !`-->
<!-- [Int!] //  compile error потому, что ! - это особенность декларации объекта и не является типом (тип - Optional). То есть это привязка к имени, а потому может быть написана только на верхнем уровне и никаких вложений -->


----
## Optional. nil
В `Swift` для обозначения отсутствия значения у переменной используется ключевое слово `nil`. Работает это с помощью
```swift
	protocol ExpressibleByNilLiteral {
	    /// Creates an instance initialized with `nil`.
	    public init(nilLiteral: ())
	}
```
Только тип `Optional` соответствует `ExpressibleByNilLiteral`. Соответствие `ExpressibleByNilLiteral` для типов, использующих `nil` для других целей, не рекомендуется.
```swift
	var variable: Int? = nil // .none
```


----
## Поток управления, проверка условий

```swift
	if condition {
		// condition is true
	} else if condition2 {
		// condition is not true, condition2 is true
	} else {
		// condition and condition2 are both false
	}
	
	guard condition3 else {
		// condition3 is not true in else block
		return // break | continue | throw
	}
	
	switch someInteger {
	case 0:
		fallthrough
	case 1..<5:
		break
	default:
		break
	}
```


----
## Поток управления, циклы

```swift
	for i in 0...9 {
	}
	while condition {
	}
	
	repeat {
	} while condition
```
* Возможны ситуации, когда внутри цикла (или проверки) вы имеете вложенные циклы и/или проверки, которые должны влиять на работу внешнего блока. Для этого предусмотрена возможность выдачи имени

```swift	
	loopName: for (key, value) in dictionary.enumerated() {
		switch value {
			case .stop:
				break loopName
			case .continue:
				continue loopName
			default: 
				break
		}
		// some logic
	}	
```


----
## Функции

* Помогают структурировать код 
* Облегчают понимание логики работы программы
* Переиспользование 
* Бывают глобальные, объектные и анонимные

<!-- 
Рассказать про по сути идентичность функций, методов и closure
про то, что можно объявить в функции функцию и что это по сути является константным closure и имя функции является именем этой константы. Хранится на стеке
-->


----
## Функции, синтаксис

```swift
	func f1(param1: Int, param2: Int) -> Int { return 0 }
	let _ = f1(param1: 0, param2: 0)
	
	func f2(_ param1: Int, param2: Int = 12) -> (Int, Bool) { return (0, false) }
	let _ = f2(0, param2: 0) // or
	let _ = f2(0)
	
	func f3(external1 param1: Int, external2 param2: Int) {}
	f3(external1: 0, external2: 0)
	
	// Можно передать >= 0 значений, в функции максимум 1 такой параметр 
	func f4(numbers: Double...) {} 
	f4(numbers: 1, 2, 3) // or
	f4(numbers: 1, 2, 3, 4, 5.5, 6)
	
	func swap(_ a: inout Int, _ b: inout Int) {}
	var var1 = 0; var2 = 1
	swap(&var1, &var2)
	
```
<!-- inout не может иметь дефолт значение, переменный по количеству значений параметр не может быть inout 

inout работает по принципу скопировали сначала, поработали, скопировали обратно
-->


----
## Функции, синтаксис
<!-- можно объявлять вложенные функции -->
```swift
	func changeByOne(increase: Bool) -> (Int) -> Int {
		func incrementFunc(value: Int) -> Int { return value + 1 }
		func decrementFunc(value: Int) -> Int { return value - 1 }
		
		return increase ? incrementFunc : decrementFunc
	}
```
<!-- Но проще использовать closure -->
```swift
	func f1(closure: @escaping () -> Void)  {
		OperationQueue.main.addOperation(closure)
	}
	
	func f2(closure: () -> Void)  {
		closure()
	}
	
	class Person {
		var age = 20
		
		func life() {
			f1(closure: {
				self.age = 21
			})

			f2(closure: {
				age = 21
			})
		}
	}
```


----
## Closures
Замыкания могут захватывать и хранить ссылки на любые константы и переменные из контекста, в котором они определены. Функции, описанные перед этим, являются по сути специальными случаями замыканий.

* Глобальная функция - замыкание, которое имеет имя и не захватывает значения
* Вложенная функция - замыкание, которое имеет имя и может захватывать значения из содержащей еë функции
* Closure - анонимное замыкание, которое может захватывать значения из окружения
<!-- тут я написал по англ чтобы разнести смысл определений. Слева (closure) - конструкция языка, а справа еë определение -->


----
## Closures, синтаксис
<!-- 
```swift
	{ (parameters) -> returnType in
		statements
	}
```
Параметры
* могут быть inout
* могут быть с переменные количеством значений, если указано имя
* могут быть кортежами

ключевое слово in означает конец декларации параметров и возвращаемого значения, и тем самым служит началом определения тела замыкания
-->
```swift
	reversed = strings.sorted(by: { (s1: String, s2: String) -> Bool in
		return s1 > s2
	})
	
	reversed = strings.sorted(by: { (s1: String, s2: 
			String) -> Bool in return s1 > s2 } ) // написано на одной строке
	
	reversed = strings.sorted(by: { s1, s2 in return s1 > s2 } ) // вывели типы
	
	reversed = strings.sorted(by: { s1, s2 in s1 > s2 } ) // отбросили return
	
	reversed = strings.sorted(by: { $0 > $1 } ) // алиас для аргументов
	
	reversed = strings.sorted() { $0 > $1 } // trailing closure
	
	reversed = strings.sorted { $0 > $1 } // пустые скобки можно убрать
	
	reversed = strings.sorted(by: >) // > - это оператор - функция
	

```


----
## Closures, захват значений
* Вложенная функция - замыкание, которое имеет имя и может захватывать значения из содержащей еë функции
```swift
	func increment(amount: Int) -> () -> Int {
		var total = 0
		func incrementNestedFunc() -> Int {
			total += amount
			return total
		}
		return incrementNestedFunc
	}
	
	let f = increment(amount: 10)
	print(f()) // 10
	print(f()) // 20
	
	let f2 = increment(amount: 10)
	print(f2()) // 10
	print(f()) // 30
```


----
## Классы и структуры

* Имеют свойства для хранения значений
* Имеют методы для предоставления функциональности
* Имеют конструкторы - возможность инициализации
* Могут быть расширены по функциональности
* Могут реализовывать протоколы (следовать контрактам)
###Только классы:
* Наследование
* Преобразование типа в рантайме (type casting)
* Деинициализация (можно освободить ресурсы доп.логикой)
* Подсчëт ссылок - один и тот же объект доступен в нескольких местах

<!-- 
	Рассказать ref & value types 
	Начать рассказ с того, что такое структура (Толя посоветовал вести речь на примере числа. Типа у тебя есть число, ты с ним работаешь и оно прямо у тебя рядом. Ты меняешь число и оно полностью меняется. Становится другим. А с классом немного по другому. Это та же структура, только лежит где-то там, в куче. И чтобы с ней работать тебе выдаëтся ссылка. Ссылка это как структура. Вот она у тебя есть и если ты еë поменяешь, то поменяется всë. Но объект по ссылке останется нетронутым. 
	Размышления на тему когда что использовать. Как общую рекомендацию для структур можно привести
	* объединение нескольких простых значений
	* поля сущности в основном value-type (поскольку мы ожидаем, что будет копирование происходить. так пусть копируется)
	* не нужно никакое наследование (свойств и поведения) от других типов
	-->


----
## Классы и структуры, синтаксис

```swift
	struct HumanMeasure {
    var weight: Float = 0
    var height: Float = 0
	}
	/* HumanMeasure(), HumanMeasure(weight: 90, height: 190) */
	
	class Person {
	    var measure = HumanMeasure()
	}
	
	let man = Person()
	var value = man.measure
	value.weight = 90
	print(man.measure.weight) // 0.0
	
	let manRef2 = man
	manRef2.measure = HumanMeasure(weight: 90, height: 190)
	print(man.measure.height) // 190.0
```
<!-- рассказать, что все поля должны иметь значение по умолчанию -->


----
## Классы и структуры, свойства

```swift
	class Person {
		private var measure = HumanMeasure() // stored property
		var weight: Float { // computed property
			get {
				return measure.weight
			}
			set { // or set(newWeight)
				measure.weight = newValue
			}
		}
		var age = 0 {
			willSet { // or willSet(newAge)
				print(newValue)
			}
			didSet { // or didSet(oldAge)
				print(oldValue)
			}
		}
		lazy var child = Person()
		static var personsNumber = 0
	}	
```


----
## Классы и структуры, методы

<!-- 
		static - нельзя переопределить в наследниках классов
class - можно 

		Рассказать про self	- неявное свойство объекта, которое является точным эквивалентом объекта, обращения к нему
-->
		
```swift
	struct Counter {
		private(set) var number = 0
		
		@discardableResult
		mutating func increment(by number: Int) -> Int { 
			self.number += number 
			return self.number
		}
		
		mutating func reset(to number: Int) {
			self = Counter(number: number)
		}
		
		static func print(counter: Counter) {
			print("The number is ", counter.number)
		}
	}
```


----
## Классы и структуры, subscript

```swift
	class Vector {
		private var components = [Double]()

		subscript(index: Int) -> Double {
			get {
				return components[index]
			}
			set {
				components[index] = newValue
			}
		}
	}
```
Может принимать любое количество параметров любого типа 


----
## Наследование

* Доступно только для классов.
* Нет множественного наследования.
* Нет универсального базового класса.

```swift
	class Shape {
		var corners = [Point]()
		func perimeter() -> Double {
			// ...
		}
	}
	
	class Square: Shape {
		override var corners = [Point]() { // get set?
			didSet {
				side = // calculate from corners value
			}
		}
	
		var side: Double = 0
		override func perimeter() -> Double {
			return 4 * side
		}
	}
```

* Пометка `final` запрещает возможность переопределения.

<!--
	также override возможен для свойств, чтобы определить свои геттеры и сеттеры, или добавить обсерверы на изменение.
	
	переопределяем сеттер - обязаны переопределить геттер. Не хотим? делаем return super.thisProperty
-->


----
## Инициализация

Процесс подготовки объекта класса, структуры или перечисления к использованию. Включает в себя установку стартовых значений для всех хранимых свойств (обязательное требование на конец инициализации), а также выполнение каких-нибудь дополнительных необходимых операций.

<!--
	Выставление значения свойству в инициализаторе\дефолтном значении не приводит к вызову обсерверов
	
	Использование дефолт значения лучше, так как сокращает код, делает установку значения ближе к объявлению, позволяет неявно определить тип данных, а также позволяет по полной воспользоваться дефолтным инициализатором и наследованием инициализаторов. Использовать, когда свойство всегда принимает одно и то же значение при создании экземляра
-->

```swift
	class Some {
		var i = 0
		var b: Bool
		var title: String? // default is nil
		
		init() { // могут быть разные параметры
			i = false
		}
		
		init(b: Bool) {
			self.b = b
		}
	}
```


----
## Инициализация
<!-- Пример создания с помощью разных инициализаторов -->
```swift
	func normalize(color: Double) -> Double {
		return max(0, min(1, color))
	}
	
	struct Color {
		let red, green, blue: Double
		
		init(red: Double, green: Double, blue: Double) {
			self.red = normalize(color: red)
			self.green = normalize(color: green)
			self.blue = normalize(color: blue)
		}
		init(white: Double) {
			self.red = normalize(color: white)
			self.green = normalize(color: white)
			self.blue = normalize(color: white)
		}
	}
	
	let yellow = Color(red: 1, green: 1, blue: 0)
	let lightGray = Color(white: 0.8)
```


----
## Инициализация

Если в структуре или классе определены значения по умолчанию для всех свойств, и при этом не определëн ни один инициализатор, то `Swift` предоставляет инициализатор по умолчанию (default initializer).

```swift

	class Object {
		var someString = "some string"
	}
	
	let object = Object()
	
```


----
## Инициализация структур
Если в структуре определены значения по умолчанию для всех свойств, и при этом не определëн ни один инициализатор, то `Swift` предоставляет инициализатор по всем свойствам (memberwise initializer).

```swift
	struct Point {
		var x = 0.0, y = 0.0
	}
		
	// как обмануть и определить свои инициализаторы:
	extension Point {
		init(ox: Double) {
			self.x = ox
		}
	}
	
	let a = Point()
	let b = Point(x: 1, y: -1.23)
	let c = Point(ox: 12)
```


----
## Назначенный инициализатор класса

* Designated initializer (DI) – главный, основной инициализатор для класса. 
* Каждый класс должен иметь как минимум один DI.
* Может быть несколько у одного класса.
* Является обязательным шлюзом, через который проходит процесс инициализации объекта перед тем, как уйти вверх по иерархии класса. К этому моменту должны быть проинициализированы **все** свойства объекта.



