import dask.dataframe as dd # 
import dask_cudf # 
import glob # 

def run_distributed_pipeline(file_pattern):
    """
    여러 개의 파일을 분산 환경에서 로드하고 MapReduce 연산을 수행합니다.
    """
    # glob을 활용하여 패턴에 맞는 여러 파일 경로를 리스트로 가져옵니다. 
    file_paths = glob.glob(file_pattern) # 
    
    if not file_paths:
        print("데이터 파일을 찾을 수 없습니다.")
        return

    print(f"Processing {len(file_paths)} files...")

    # 1. Dask-cuDF를 이용한 다중 파일 병렬 로딩 (Lazy Evaluation)
    # 데이터를 파티션으로 나누어 워커에 할당할 준비를 합니다. 
    ddf_gpu = dask_cudf.read_csv(file_paths, header=0) # 
    ddf_gpu.columns = ["Date Time", "Water Level", "Sigma"] # 
    
    # 2. Map Operation (비동기 병렬 변환)
    # 각 워커가 독립적으로 연산을 수행합니다. (예: Water Level + 10) 
    map_step = ddf_gpu["Water Level"] + 10 # 
    
    # (선택) DAG 시각화 저장 - Dask가 구성한 작업 흐름을 확인합니다.
    # map_step.visualize(filename="images/mapreduce_dag.png") # 
    
    # 3. Reduce Operation (동기화 및 집계)
    # 분산된 데이터를 통신하여 최종 합계를 구합니다. compute() 호출 전까지는 연산되지 않습니다. 
    final_result = map_step.sum().compute() # 
    
    print(f"최종 집계 결과(Sum): {final_result}")
    return final_result

if __name__ == "__main__":
    # 실행 예시 (여러 개의 CSV 파일이 있는 경로 지정)
    # run_distributed_pipeline("data/*.csv") # 
    pass
