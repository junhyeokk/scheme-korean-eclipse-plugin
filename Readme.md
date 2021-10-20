# Korean Scheme interpreter and Eclipse plugin
## 개요
2021년 1학기 정보컴퓨터공학과 공학연구실습 과정을 통해 만들어진 scheme 한글버전 코드입니다.
* scheme-kr-interpreter 폴더에는 참고사이트(https://www.lwh.jp/lisp/index.html)의 내용을 바탕으로 Chapter 8: Booleans and short-circuit evaluation까지의 기능이 Python으로 구현되어 있습니다.
* schemetest 폴더에는 이클립스에 설치할 플러그인의 개발 코드가 포함되어 있습니다.
* distribution-jar 폴더에는 이클립스에 플러그인을 설치할 수 있도록 빌드된 jar 파일이 포함되어 있습니다.
Windows10, Python 3.8.5, Eclipse IDE for Eclipse Committers (2021-03 4.19.0) 환경에서 개발 및 테스트되었습니다.
<br/><br/>
## 설치방법
eclipse-plugin을 설치하는 것과 interpreter를 설치하는 두 단계를 거쳐 설치를 진행합니다.
1. eclipse-plugin 설치
* jar 파일을 이용해 설치하는 방법<br/>
    distribution-jar 폴더 안의 jar 파일을 이클립스가 설치된 경로의 dropins 폴더 안으로 복사한 뒤 이클립스를 재시작합니다.
* 이클립스의 플러그인 설치기능을 이용하는 방법<br/>
eclipse에서 Help > Install New Software...에 들어간 뒤 Add...버튼을 클릭하고 Location에 배포 폴더의 URL을 복사해 넣고 Add를 누릅니다.
(https://github.com/schemeway/SchemeScript 의 Installation 항목 참조)
현재 배포 서버가 준비되지 않아 사용할수 없습니다.
2. 한글 Scheme 인터프리터 설치<br/>
scheme-kr-interpreter폴더를 C 드라이브 하위에 추가합니다.
<br/><br/>
## 한글 Scheme 예약어 / 내장함수
* define → ㅋ<br/>
함수 등을 define할 때 사용되는 키워드이므로 함수를 나타내는 f와 닮은 한글인 ㅋ으로 상형
* lambda → ㅅ<br/>
람다의 수학 기호와 닮은 한글인 ㅅ으로 상형
* if → ㄷ<br/>
if가 참일때와 거짓일때에 따라 분기시키는 역할을 하므로 두 갈래로 나뉘는 모양인 ㄷ으로 상형
* quote → ㅇ<br/>
가장 간단한 모양인 ㅇ으로 상형
* car → ㅓ<br/>
car가 pair에서 앞쪽의 원소를 반환하므로 앞을 가리키는 ㅓ으로 상형
* cdr → ㅏ<br/>
cdr가 pair에서 뒷쪽의 원소를 반환하므로 뒤를 가리키는 ㅏ으로 상형
* cons → ㅐ<br/>
cons는 두 원소를 합쳐 하나의 pair로 반환하므로 car와 cdr를 합친 모양인 ㅐ으로 상형
<br/><br/>
## 테스트 방법
이클립스 내의 Window > Show view > Other으로 들어간 뒤 PNU scheme p21-01 > scheme interpreter를 선택한 뒤 Open을 클릭합니다.
### 테스트 코드
* 제곱
```
(ㅋ 제곱 (ㅅ (인자) (* 인자 인자)))
(제곱 3)
```
* 팩토리얼
```
(ㅋ 팩토리얼
(ㅅ (인자)
(ㄷ (= 인자 0) 1 (* 인자 (팩토리얼 (- 인자 1))))))
(팩토리얼 5)
```
* 함수형 프로그래밍
```
(ㅋ 덧셈제조기 (ㅅ (변수일) (ㅅ (변수이) (+ 변수일 변수이))))
(ㅋ 더하기이 (덧셈제조기 2))
(더하기이 5)
```
<br/>

## 개발과정
https://pllab.tistory.com/
