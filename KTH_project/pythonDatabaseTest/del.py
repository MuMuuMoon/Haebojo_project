            #찾은객체 상자
            cv2.rectangle(img, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
            #객체 이름상자
            cv2.rectangle(img, (int(bbox[0]), int(bbox[1]-30)), (int(bbox[0])+(len(class_name)+len(str(track.track_id)))*17, int(bbox[1])), color, -1)

            cv2.putText(img, class_name + "-" + str(track.track_id),(int(bbox[0]), int(bbox[1]-10)),0, 0.75, (255,255,255),2)

            #datas[0]에는 라벨링된 id정보가 들어가고
            #datas[1]에는 [0]에서 라벨링된 사람의 x좌표
            #datas[2]에는 [0]에서 라벨링된 사람의 y좌표
            #빈리스트에 라벨링번호,x좌표,y좌표를 담은뒤
            listval.append("p")
            listval.append(str(track.track_id))
            listval.append(str(round(bbox[0])))
            listval.append(str(round(bbox[1])))
            #datas라는 1부터 차례대로 증가되는 딕셔너리에 listval 를 통째로 벨류값으로 넣는다

            datas[i]=listval
            #아까 위에서 채워진 리스트를 비워서 새로이 datas에 1이 증가된 다음키값으로 키 벨류 형태로 넣기위해 초기화진행
            listval=[]
            # 인식된 객체들 좌표 출력하기
            # print(bbox[0], bbox[1],bbox[2],bbox[3])
            #i에 1을 더해주는이유는 1.총카운트숫자 알아내기 2.datas에 벨류값들을 추가할때 키값이1씩증가하는것이 필요하니까
            i+=1
            print(str(track.track_id) + "  <<  person number  -  [ x , y ] 좌표>>  [ " + str(round(bbox[0])) + "  , " +str(round( bbox[1]))+" ]")

        #태훈 추가코드 시작

        data['p']="p"
        datas[0]=i
        requests.post(url,data=datas)


        #태훈 추가코드 종료
        print("ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n")