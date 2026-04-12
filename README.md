# BLM5027 Assignment 1 - Reinforcement Learning with Taxi-v3 on a 6x6 Grid
Bu projede OpenAI'a ait olan Gym (Gymnasium fork'u üzerinden devam ettiriliyor) kütüphanesindeki Taxi-v3 ortamını 6x6 boyutunda olacak şekilde tekrardan tasarlayarak Q-Learning algoritması ile eğiteceğiz.

## Proje Detayları
Taxi-v3 ortamı, otonom bir taksinin işleyişini minimalist bir şekilde modellemek için tasarlanmıştır. Bu model üzerinde taksinin davranışlarını eğiterek

Her hangi bir durumda taksimiz 6 farklı eylemden birini gerçekleştirebilir ve bu eylemlere göre ödüllendirilir ya da cezalandırılır:
- 0: Sola İlerle    (-1 Puan)
- 1: Sağa İlerle    (-1 Puan)
- 2: Yukarı İlerle  (-1 Puan)
- 3: Aşağı İlerle   (-1 Puan)
- 4: Yolcuyu Bırak  (Yolcuyu hedef noktaya bırakırsa +20 Puan, yanlış durakta bırakırsa -1 Puan, yolcunun bırakamayacağı bir yerde uygulanırsa -10 Puan)
- 5: Yolcuyu Al     (-1 Puan, yolcunun olmadığı bir yerde uygulanırsa -10 Puan)

Yolcu, haritadaki duraklar arasından bir tanesine yerleştirilir ve duraklardan bir tanesi hedef olarak belirlenir. Yolcunun olabileceği durum, her bir durağın yanı sıra taksinin içerisi de olabileceğinden ötürü (n+1) adettir.

Amacımız, taksimizi elimizdeki harita üzerinde önce bulunduğu duraktan yolcuyu alacak ondan sonra da hedef noktasına götürüp bırakacak şekilde eğitebilen bir model tasarlamak ve çalıştırmaktır.

## Model Yapısı
Projede Q-Learning yaklaşımı kullanılmıştır. Bu yöntemde her durum-eylem çifti için bir değer tutulur ve ajan zamanla hangi durumda hangi eylemin daha avantajlı olduğunu öğrenir. Yazdığımız kod herhangi boyutta bir grid ve durak sayısına izin verse bu proje için 6x6 bir grid kullanacağız ve bu grid üzerinde 5 farklı durak belirleyeceğiz.

Durum uzayı şu bileşenlerden oluşmaktadır:
- taksinin x koordinatı  (6 -> 6)
- taksinin y koordinatı  (6 -> 36)
- yolcunun durumu        (5+1 -> 216)
- hedef konumu           (5 -> 1080)

Her durum için 6 farklı aksiyon bulunduğu için Q-tablosunun boyutu (1080, 6) şeklindedir.

Q-Learning güncellemesi standart formülle yapılmaktadır:
Q(s, a) = (1 - _α_) * Q(s, a) + _α_ * (_r_ + _γ_ * max(Q(s')))

s : Şu anki durum\
a : Şu anki eylem\
s': Bir sonraki durum

_α_: learning rate (öğrenme oranı) [0.1]\
_γ_: discount factor (indirim faktörü) [0.95]\
_r_: reward (bu durumdaki alınan ödül)

```
def update_q_table(old_state, old_value, next_value, reward):
        Taxi.q_table[old_state, Taxi.action] = (1 - Taxi.learning_rate) * old_value + Taxi.learning_rate * (reward + Taxi.discount_factor * next_value)
```

Eylem seçimi için Epsilon Greedy algoritmasından yararlanacağız. Bu algoritmada verilen bir _ε_ değerine oranla model ya öğrendiği bilgiler arasından en optimal olanı yapar ya da rastgele eylemler gerçekleştirerek yeni bilgi edinmeye çalışır.

_ε_: Epsilon [0.95 -> 0.01, Decay rate = 0.05%]

```
if rnd.uniform(0, 1) < Taxi.epsilon:
        Taxi.action = rnd.randrange(6)
else:
        Taxi.action = np.argmax(Taxi.q_table[old_state])
```

Grafiksel gösterim üzerinde n adet durak 0 ile n-1 arasında sayısal değerler ile grid üzerinde gösterilir. Bu durakların yanında eğer yolcu bulunuyor ise _p_, eğer bu durak hedef konum ise _d_ harfi bulunur. Taksi grid üzerinde yolcuyu taşıyorsa _T_ ile, taşımıyorsa da _t_ ile, bunların dışındaki bütün boş noktalar _:_ ile gösterilir.

## Eğitim Süreci ve Sonuçlar
Toplamda 10,000 episode'dan (bölümden) oluşan bir eğitim süreci sonucunda modelin ortalama ödül değeri -500 civarından +10 civarına kadar iyileşme göstermiştir ve _ε_ değeri azaldıkça daha tutarlı hareketler göstermiştir. Yapılan adımlar daha akıllıca ve daha tutarlı bir hale gelmeye başladıkça da her bir episode'un süresi üstel olarak daha kısa sürmeye başlamıştır.

<p align="center">
<img width="365" height="197" alt="Screenshot (4702)" src="https://github.com/user-attachments/assets/7fd43a7f-d158-4101-827e-3bca4b362d9d" />  
        
<p align="center">
<img width="514" height="277" alt="Screenshot (4701)" src="https://github.com/user-attachments/assets/5610cc4e-f1e9-4efd-92c8-0075b200572b" />
        
<p align="center">
<img width="220" height="220" alt="taxi_gif1" src="https://github.com/user-attachments/assets/10f57f86-4f34-463a-ba37-b4e29bbd9809" />
        
<img width="220" height="220" alt="taxi_gif2" src="https://github.com/user-attachments/assets/d963bff7-b5c1-41b5-9823-15e26b126423" />

