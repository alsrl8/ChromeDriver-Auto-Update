# ChromeDriver Auto Update

Chromedriver RESTful API를 사용하여 chromedriver stable version을 자동으로 다운로드하는 프로그램입니다.
이 프로그램은 `Windows` 환경에서 제작되었습니다.
---

### Usage
```angular2html
python main.py
```

### Chromedriver

이 프로그램은 `Stable` ChromeDriver를 최신 버전으로 자동 업데이트합니다. 버전 비교 시 ChromeDriver 버전의 첫 번째 숫자만을 사용합니다. 예를 들어, 현재 시스템에 설치된 ChromeDriver 버전이 `119.0.6045.105`이고, 사용 가능한 최신 버전이 `120.x.x.x`라면, 첫 번째 숫자가 다르기 때문에 자동으로
업데이트를 진행합니다. 하지만 최신 버전이 `119.x.x.x`인 경우에는 업데이트를 하지 않습니다.

이 로직은 크롬 브라우저와 ChromeDriver 간의 주요 호환성을 보장하기 위해 설계되었습니다. 크롬 브라우저의 주요 버전 업데이트는 첫 번째 숫자의 변경을 통해 이루어지므로, 이를 기준으로 ChromeDriver의 업데이트 여부를 결정합니다.

```
C:\> chromedriver.exe --version
>>> ChromeDriver 119.0.6045.105
```
---
### Deprecated

Python Selenium이 chromedriver 자동 업데이트를 지원하면서 이 프로젝트는 종료되었습니다. ㅠㅠ
