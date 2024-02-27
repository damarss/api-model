def encode_data(input_data, encoder, pd):
    # memisahkan data dengan tipe object
    input_data_not_obj = input_data.select_dtypes(exclude=['object'])
    input_data_obj = input_data.select_dtypes(include=['object'])

    # encode data dengan tipe object
    input_data_obj_encoded = encoder.transform(input_data_obj).toarray()
    input_data_obj_encoded = pd.DataFrame(input_data_obj_encoded, columns=encoder.get_feature_names_out(input_data_obj.columns))
    input_data_obj_encoded.set_index(input_data_obj.index, inplace=True)

    # menggabungkan data
    input_data_encoded = pd.concat([input_data_not_obj, input_data_obj_encoded], axis=1)

    return input_data_encoded