# 1. Введение в Swift

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
## Перечисления


----
## Optional
```swift
enum Optional<T> {
	case some(T)
	case none
}
```


----
## Коллекции
<!-- Слайд для напоминания синтаксиса --->

Для создания массивов и словарей используются `[]`
```swift
	// Array<String>
	let array = ["cat", "dog"]
	let emptyArray = [String]()
	let emptyArray2: [String] = []
	
	// Dictionary<String, Int>; Key must be Hashable
	let dictionary = ["key1": 7, "key2": 14, "key3": 21]
	let emptyDictionary = [String: Int]() 
	let emptyDictionary2: [String: Int] = [:]
```





----
## Поток управления, проверка условий

```swift
	if condition {
	}
	
	enum Some {
		case one, two, three
	}
	
	switch someValue {
	case .one:
		fallthrough
	case .two:
		break
	default:
		break
	}
```








