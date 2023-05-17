# Classy
Yet another simplest dataclass-like object for Python.

<br>

> ### **Classy** is a simplest dataclass with a several **restriction**.  
> 1. **Constructor** of Classy object only available with **keyword argument**.  
> 2. Classy object is not *"Auto Hashable"* nor *"Auto Equatable"*. You have to implement *compute_hash(self)* or *equals(self, __o: object)* method on your own.  
> 3. Classy object has to be decorated with **mutability decorator**. You need to set @mutable or @immutable decorator in your class definition.  
> ```python
> from classy import Classy, mutable, immutable
>
> @mutable  # You have to decorate with this when you want to keep this object mutable
> class MutableClass(Classy):
>     name: str
> 
> @immutable  # You have to decorate with this when you want to keep this object immutable
> class ImmutableClass(Classy):
>     name: str
> 
> a: MutableClass = MutableClass(name="John")  # Classy object must be constructed with keyword argument.
> a.name = "Sarah"  # It is OK to mutate it's field with @mutable decorator.
> 
> b: ImmutableClass = ImmutableClass(name="John")  # Classy object must be constructed with keyword argument.
> b.name = "Sarah"  # This will raise 'dataclasses.FrozenInstanceError'
> assert a == a  # This will raise NotImplementedError. You have to implement equals(self, __o: object) -> bool:
>```  

<br>

> ### Why **Classy** has restriction?  
> **Classy** is designed to develop domain models with minimum overhead.  
> **Classy** is a just a wrapper for *dataclasses.dataclass* and uses *typing.dataclass_transform*  
> Also, **Classy** is only uses pure python builtins, So you can keep your domain area safe from other dependencies.  
> **Classy** doesn't use metaclass to modify default type instantiator of your class. So It is truly pure **Plain Old Python Object**.  
> I think **explicit** is better than **implicit**.  
> So, **Classy** restricts its own constructor to use **keyword argument only**. This may helps your project's coding convention.  
> And also helps your teammate to prevent their **tiny mistake** (wrong placing argument's position)  

<br>

> ### What **Classy** can actually do?
> Pretty much nothing.  
> But **Classy** has some features might useful for your project.  
> 1. Classy has *.dict* or *.json* property to serialize.  
> 2. Classy has classmethod *default()*. So, you can create object with default value.  
> 3. Classy has classmethod *from_dict()* or *from_json()* to deserialize your object.  
> 4. You can change default json serializer to override *serialize()* and *deserialize()* (currently use builtin json module)
> 5. You can override *equals()* or *compute_hash()* to support hashing and equatable.  
